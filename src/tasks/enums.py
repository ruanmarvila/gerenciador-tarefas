import enum


class TaskStatus(enum.StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

    @property
    def formated(self):
        FORMATED_MAP = {
            TaskStatus.TODO: "Todo",
            TaskStatus.IN_PROGRESS: "In Progress",
            TaskStatus.DONE: "Done"
        }
        return FORMATED_MAP.get(self, self.value)
    
class TaskColumn(enum.StrEnum):
    TITLE = "title"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"

class TaskOrder(enum.StrEnum):
    ASCENDING = "asc"
    DESCENDING = "desc"