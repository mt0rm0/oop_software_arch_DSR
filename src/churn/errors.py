class DataPipelineError(Exception):
    pass


class LoadingDataError(DataPipelineError):
    def __init__(self):
        super().__init__("Something went wrong while loading the file.")


class ColumnValidationError(DataPipelineError):
    def __init__(self):
        super().__init__("Could not validate schema for some reason.")


class CleaningDataError(DataPipelineError):
    def __init__(self, col_name: str) -> None:
        self.col_name = col_name
        super().__init__(
            f"Something went wrong during cleaning the column'{self.col_name}."
        )


class WrongDataTypeError(CleaningDataError):
    def __init__(self, col_name: str) -> None:
        super().__init__(col_name)
