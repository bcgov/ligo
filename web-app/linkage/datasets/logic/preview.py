import pandas as pd
import random
import numpy as np
from django.conf import settings

PD_PSQL_TYPE_MAP = {
    "object"    : "VARCHAR",
    "int64"     : "INTEGER",
    "float64"   : "REAL",
    "bool"      : "BOOLEAN",
    "int8"      : "SMALLINT"
}

SQL_PANDAS_MAP = {
    "VARCHAR": object,
    "BOOLEAN": np.bool_,
    "REAL": np.float64,
    "INTEGER": np.int64,
    "CHAR": object,
    "TEXT": object,
}

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Previewer(object):

    @staticmethod
    def create_previewer(filename, data_format):
        previewers = {'csv': CSV_Previewer}
        return previewers[data_format](filename)

    def __init__(self, filename, format):
        self.format = format
        self.filename = filename
        self.data = None
        self.row_count = 0

    def preview(self, criteria='head', limit=100):
        NotImplemented


class CSV_Previewer(Previewer):

    def __init__(self, filename):
        super(CSV_Previewer, self).__init__(filename, 'csv')

    def preview(self, criteria='head', limit=100, data_types=None):

        from io import StringIO
        # in Python 2 use
        #from StringIO import StringIO

        def load_with_buffer(filename, skip, **kwargs):
            s_buf = StringIO()
            with open(filename) as file:
                count = -1
                for line in file:
                    count += 1
                    if skip[count]:
                        continue
                    s_buf.write(line)
            s_buf.seek(0)
            df = pd.read_csv(s_buf, **kwargs)
            return df

        """
        Selects a subset of rows from the given csv file based on the given criteria. The number of selected rows is
        defined by limit parameter. Default value is 100. If no criteria is provided, it will select the rows from
        the head of file.
        :param file_name: The name/path of dataset file.
        :param criteria: Row Selection Criteria. 'head' : Selects a subset of rows from the beginning of the file.
                        'tail' : Selects a subset of rows from the end of file.
                        'rand' : Randomly selects a sunset of rows.
        :param limit: The maximum number of records that must be returned.
        :return: Selected subset of rows.
        """

        if self.filename is None:
            raise IOError('Dataset filename is missing')

        logger.info('Data type: '.format(data_types))

        # Load the csv file
        file_path = settings.DATASTORE_URL + self.filename
        self.row_count = sum(1 for row in open(file_path))

        if limit > self.row_count:
            limit = self.row_count

        # Mapping of row selection criteria to the selecting functions.
        # does not sound right for limit > self.row_count case mentioned above
        # I guess that scenario has never been tested.
        selection = {
            'head': range(limit + 1, self.row_count + 1),
            'tail': range(1, self.row_count - limit),
            'rand': sorted(random.sample(range(1, self.row_count + 1), self.row_count - limit))
        }
        skip_list = selection.get(criteria, None)

        skip_list = np.asarray(skip_list, dtype=np.int64)
        # MAX >= number of rows in the file
        skip_mask = np.zeros(self.row_count + 1, dtype=bool)
        skip_mask[skip_list] = True

        # Convert SQL data types to Pandas data types
        d_types = None
        if data_types:
            d_types = {}
            for col_name, col_type in data_types.items():
                d_types[col_name] = SQL_PANDAS_MAP[col_type]

        result = pd.read_csv(file_path, skiprows=skip_list, skipinitialspace=True, dtype=d_types)
        result = result.replace(np.nan, '', regex=True)
        header_types = {}

        for (key, value) in result.dtypes.items():
            header_types[key] = PD_PSQL_TYPE_MAP.get(value.name)
        return {
            'len': self.row_count,
            'header': list(result),
            'rows': result.values.tolist(),
            'types': header_types
        }


def get_preview(filename, data_format):
    return Previewer.create_previewer(filename, data_format)
