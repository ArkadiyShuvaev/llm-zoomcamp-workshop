from dataclasses import dataclass


@dataclass
class RetrievalResult():
    score: int
    section: str
    course: str
    question: str
    answer: str

    def __str__(self):
        return (
            f"RetrivalResult: score={self.score}, section={self.section}, "
            f"course={self.course}, question={self.question}, "
            f"answer={self.answer}"
        )
