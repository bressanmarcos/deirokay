from pandas import DataFrame, Series


class DeirokaySeries(Series):

    _internal_names = Series._internal_names + []
    _internal_names_set = set(_internal_names)

    _metadata = []

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

    @property
    def _constructor(self):
        return DeirokaySeries

    @property
    def _constructor_expanddim(self):
        return DeirokayDataFrame


class DeirokayDataFrame(DataFrame):
    """
    DeirokayDataFrame class
    """
    _internal_names = DataFrame._internal_names + []
    _internal_names_set = set(_internal_names)

    _metadata = []

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

    @property
    def _constructor(self):
        return DeirokayDataFrame

    @property
    def _constructor_sliced(self):
        return DeirokaySeries
