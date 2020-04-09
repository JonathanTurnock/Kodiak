class Comment:
    def __init__(self, id, author, content):
        self.id = id
        self.author = author
        self.content = content


class CommentsDao:
    def __init__(self):
        self.comments = {
            '1': Comment(id=1, author="Billy", content="Hello World"),
            '2': Comment(id=2, author="Joe", content="Goodbye World")
        }

    def get_comments(self):
        return self.comments.values()


comments_dao = CommentsDao()
