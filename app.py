from fastapi import FastAPI, Header, Cookie, Request, HTTPException, status, Form
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.models import session, User, Post, engine

app = FastAPI()
templates = Jinja2Templates(directory="templates")
engine.connect()


# Главная страница
@app.get("/")
async def home(request: Request):
    return RedirectResponse("/users")


# === CRUD для Users ===

@app.get("/users")
async def users(request: Request):
    users = session.query(User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/new")
async def newUser(request: Request):
    return templates.TemplateResponse("UserForm.html", {"request": request, "message": ""})


@app.post("/users/new")
async def createUser(request : Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        new_user = User(username=username, email=email, password=password)
        session.add(new_user)
        session.commit()
        return RedirectResponse("/users/", status_code=303)
    except:
        session.rollback()
        return templates.TemplateResponse("UserForm.html", {"request": request, "message": "Ошибка при добавлении, попробуйте ввести корректные данные"})



@app.get("/users/edit")
async def changeUser(request: Request, user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("UserForm.html", {"request": request, "user": user})

@app.post("/users/edit")
async def updateUser(request:Request, user_id: int, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    a = await request.form()
    user = a.get("user")
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.username = username
        user.email = email
        user.password = password
        session.commit()
        return RedirectResponse("/users", status_code=303)
    except:
        session.rollback()
        return templates.TemplateResponse("UserForm.html", {"request": request, "user": user})

@app.get("/users/delete")
async def deleteUser(user_id: int):
    print(user_id)
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    for i in posts:
        session.delete(i)
        session.commit()
    session.delete(user)
    session.commit()
    return RedirectResponse("/users", status_code=303)


# === CRUD для Posts ===

@app.get("/posts")
async def posts(user_id:int, request: Request):
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    user = session.query(User).filter(User.id == user_id).first()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts, "user": user})

@app.get("/posts/new")
async def newPost(user_id: int, request: Request):
    user = session.query(User).filter(User.id == user_id).first()
    return templates.TemplateResponse("PostForm.html", {"request": request, "user": user})


@app.post("/posts/new")
async def createPost(request: Request, user_id: int, title: str = Form(...), content: str = Form(...)):
    a = await request.form()
    user = session.query(User).filter(User.id == user_id).first()
    try:
        new_post = Post(title=title, content=content, user_id=user.id)
        session.add(new_post)
        session.commit()
        return RedirectResponse("/posts?user_id=" + str(user_id), status_code=303)
    except:
        session.rollback()
        return templates.TemplateResponse("PostForm.html", {"request": request, "user": user})



@app.get("/posts/edit")
async def changePost(request: Request, post_id: int, user_id:int):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("PostForm.html", {"request": request, "post": post})


@app.post("/posts/edit")
async def updatePost(request: Request, post_id: int, user_id: int, title: str = Form(...), content: str = Form(...)):
    a = await request.form()
    SavedPost = a.get("post")
    user = session.query(User).filter(User.id == user_id).first()
    try:
        post = session.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        post.title = title
        post.content = content
        post.user_id = user.id
        session.commit()
        return RedirectResponse("/posts?user_id="+str(user.id), status_code=303)
    except Exception as ex:
        session.rollback()
        print(ex.args)
        return templates.TemplateResponse("PostForm.html", {"request": request, "post": SavedPost})

@app.get("/posts/delete")
async def deletePost(post_id: int):
    post = session.query(Post).filter(Post.id == post_id).first()
    user_id = post.user_id
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return RedirectResponse("/posts?user_id=" +str(user_id), status_code=303)
