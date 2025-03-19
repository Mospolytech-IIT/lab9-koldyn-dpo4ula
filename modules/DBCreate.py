from modules.models import session, User, Post

def DropAll():
    for i in session.query(User).all():
        DeleteUserPosts(i.id)
        session.query(User).filter(User.id==i.id).delete()
        session.commit()
#Напишите программу, которая добавляет в таблицу Users несколько записей с разными значениями полей username, email и password.
def AddUsers():
    users = [
        User(username="111", email="111@222.com", password=111),
        User(username="222", email="222@222.com", password=111),
        User(username="333", email="333@222.com", password=111),
    ]
    session.add_all(users)
    session.commit()

#Напишите программу, которая добавляет в таблицу Posts несколько записей, связанных с пользователями из таблицы Users.
def AddPosts():
    posts = [
        Post(title="postic1", content="lalalalalalal", user_id=1),
        Post(title="postic2", content="lalalalalalal", user_id=1),
        Post(title="postic3", content="lalalalalalal", user_id=2),
        Post(title="postic4", content="lalalalalalal", user_id=2),
        Post(title="postic5", content="lalalalalalal", user_id=3),
    ]
    session.add_all(posts)
    session.commit()

#Напишите программу, которая извлекает все записи из таблицы Users.
def GetUsers():
    users = session.query(User).all()
    for user in users:
        return f"ID: {user.id}, Username: {user.username}, Email: {user.email}"

#Напишите программу, которая извлекает все записи из таблицы Posts, включая информацию о пользователях, которые их создали.
def GetPosts():
    posts = session.query(Post).all()
    for post in posts:
        return f"Post ID: {post.id}, Title: {post.title}, User: {post.user.username}"

#Напишите программу, которая извлекает записи из таблицы Posts, созданные конкретным пользователем.
def GetUserPosts(user_id):
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    for post in posts:
        return f"Post ID: {post.id}, Title: {post.title}, Content: {post.content}"

#Напишите программу, которая обновляет поле email у одного из пользователей.
def UpdateEmail(user_id, new_email):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        session.commit()
        return f"Email пользователя с ID {user_id} обновлен."
    else:
        return "Пользователь не найден."

#Напишите программу, которая обновляет поле content у одного из постов.
def UpdateContent(post_id, new_content):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        session.commit()
        return f"Контент поста с ID {post_id} обновлен."
    else:
        return "Пост не найден."

#Напишите программу, которая удаляет один из постов.
def DeletePost(post_id):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.delete(post)
        session.commit()
        return f"Пост с ID {post_id} удален."
    else:
        return "Пост не найден."

#Напишите программу, которая удаляет пользователя и все его посты.
def DeleteUserPosts(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.query(Post).filter(Post.user_id == user_id).delete()
        session.delete(user)
        session.commit()
        return f"Пользователь с ID {user_id} и его посты удалены."
    else:
        return "Пользователь не найден."

def generate():
    DropAll()
    AddUsers()
    AddPosts()

    print(f"Все пользователи: {GetUsers()}")
    print(f"Все посты:{GetPosts()}")
    print(f"Посты пользователя с ID 1:{GetUserPosts(1)}")
    print(f"Обновление email пользователя 1:{UpdateEmail(1, "email@email.com")}")
    print(f"Обновление контента поста:{UpdateContent(1, "Updated content for post 1")}")
    print(f"Удаление поста:{DeletePost(2)}")
    print(f"Удаление пользователя и его постов:{DeleteUserPosts(3)}")

generate()