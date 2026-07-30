class ChurnPipeline:
    def __init__(
        self,
        req_cols: list[str],
        random_state: str = 42,
    ):
        pass

    def fit(self):
        self._column_validation()
        self._label_encoding()
        self._totalcharges_fixer()

    def transform(self):
        self._column_validation()
        self._label_encoding()
        self._totalcharges_fixer()

    def fit_transform(self):
        pass

    def train(self):
        pass

    def _column_validation(self):
        pass

    def _label_encoding(self):
        pass

    def _totalcharges_fixer(self):
        pass
