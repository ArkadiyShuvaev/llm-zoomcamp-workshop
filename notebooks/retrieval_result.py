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
            f"Section={self.section}, "
            f"Question={self.question}, "
            f"Answer={self.answer}, "
            f"Score={self.score}"
        )
