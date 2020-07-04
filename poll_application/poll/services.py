from poll_application.models import User, db, Poll, \
    Question, Answer, Tag

def save_poll(obj, user):
    new_poll = Poll(
        title=obj.title,
        user_id=user.id,
        close_date=obj.close_date)

    db.session.add(new_poll)
    db.session.commit()
    return new_poll


def save_questions(obj, poll):
    for _question in obj.questions:
        question = Question(
            question=_question.capitalize(),
            poll_id=poll.id)

        db.session.add(question)
        db.session.commit()


def save_tags(obj, poll):
    for _tag in obj.tags:
        _tag = _tag.lower()
        tag = Tag.query.filter_by(title=_tag).first()
        if not tag:
            tag = Tag(title=_tag)
            db.session.add(tag)
            db.session.commit()
        poll.tags.append(tag)
        
    db.session.add(poll)
    db.session.commit()    