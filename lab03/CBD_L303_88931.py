from cassandra.cluster import Cluster
from cassandra import ReadTimeout

# connecting with cluster
cluster = Cluster()
session = cluster.connect()
session.set_keyspace("cbd")

# test connection with read command
videos = session.execute("select id, author from video")
print(
    "================================================================\nResult of query 1)"
)
for (_id, author) in videos:
    print(_id, author)
print("================================================================\n")


# alinea (a)

## inserts

### insert into user
session.execute(
    "insert into user (username, email, added_date) values (%s, %s, %s)",
    ("vr", "vascoalramos@email.pt", "2019-11-21"),
)
users = session.execute("select * from user")
print("================================================================")
print("Users Table")
print("{:16s} {:28s} {:s}".format("Username", "Added Date", "Email"))
for (userame, added_date, email) in users:
    print("{:16s} {:28s} {:s}".format(userame, str(added_date), email))
print("================================================================\n")

### insert into video
session.execute(
    "insert into video (id, author, name, description, tag, followers, total_rating, count_rating, added_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (
        11,
        "vr",
        "Spectacular video!",
        "Awesome",
        {"new_tag"},
        {"joaovasconcelos", "ds"},
        120,
        10,
        "2019-11-28",
    ),
)
videos = session.execute("select author, name, description from video")
print("================================================================")
print("Videos Table")
print("{:16s} {:20s} {:s}".format("Author", "Name", "Description"))
for (author, name, description) in videos:
    print("{:16s} {:20s} {:s}".format(author, name, description))
print("================================================================\n")

### insert into author_video
session.execute(
    "insert into author_video (id, author, name, description, tag, followers, total_rating, count_rating, added_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (
        11,
        "vr",
        "Spectacular video!",
        "Awesome",
        {"new_tag"},
        {"joaovasconcelos", "ds"},
        120,
        10,
        "2019-11-28",
    ),
)
videos = session.execute("select author, name, description from author_video")
print("================================================================")
print("Author-Videos Table")
print("{:16s} {:20s} {:s}".format("Author", "Name", "Description"))
for (author, name, description) in videos:
    print("{:16s} {:20s} {:s}".format(author, name, description))
print("================================================================\n")

### insert into tag_video
session.execute(
    "insert into tag_video (tag, videos, n_videos, added_date) values (%s, %s, %s, %s)",
    ("new_tag", {11}, 1, "2019-11-28"),
)
tags = session.execute("select tag, added_date, n_videos, videos from tag_video")
print("================================================================")
print("Tags Table")
print("{:10s} {:20s} {:<13s} {:s}".format("Tag", "Added Date", "N of Videos", "Videos"))
for (tag, added_date, n_videos, videos) in tags:
    print(
        "{:10s} {:20s} {:<13d} {:s}".format(tag, str(added_date), n_videos, str(videos))
    )
print("================================================================\n")

### insert into comment
session.execute(
    "insert into comment (video_id, author, commment_text, added_date) values (%s, %s, %s, %s)",
    (11, "ds", "Meeh", "2019-11-28"),
)

### insert into comment_video_time
session.execute(
    "insert into comment_video_time (video_id, author, commment_text, added_date) values (%s, %s, %s, %s)",
    (11, "ds", "Meeh", "2019-11-28"),
)

### insert into comment_author_time
session.execute(
    "insert into comment_author_time (video_id, author, commment_text, added_date) values (%s, %s, %s, %s)",
    (11, "ds", "Meeh", "2019-11-28"),
)

### insert into comment_video_author
session.execute(
    "insert into comment_video_author (video_id, author, commment_text, added_date) values (%s, %s, %s, %s)",
    (11, "ds", "Meeh", "2019-11-28"),
)


## queries

### get username, email and added_date from user vr
query = "select * from user where username = %s"
future = session.execute_async(query, ["vr"])
try:
    username, added_date, email = future.result().one()
    print(
        "================================================================\nResult of query 2)"
    )
    print(username, email, added_date)
    print("================================================================\n")
except ReadTimeout:
    print("Query timed out:")

### get all comments from the video 4, followed by user vascoalramos
query = "select * from following_video_comments where user = %s and video_id = %s"
future = session.execute_async(query, ["ds", 4])
try:
    user, video_id, comments = future.result().one()
    print(
        "================================================================\nResult of query 3)"
    )
    print(user, video_id, comments)
    print("================================================================\n")
except ReadTimeout:
    print("Query timed out:")

### get all videos tagged with trailer
query = "select * from tag_video where tag = %s"
future = session.execute_async(query, ["trailer"])
try:
    tag, added_date, n_videos, videos = future.result().one()
    print(
        "================================================================\nResult of query 4)"
    )
    print(tag, added_date, n_videos, videos)
    print("================================================================\n")
except ReadTimeout:
    print("Query timed out:")


## updates

### update user email
query = "update user set email = %s where username = %s"
session.execute(query, ["vascoalramos@outlook.pt", "vr"])
users = session.execute("select * from user")
print("================================================================")
print("Users Table")
print("{:16s} {:28s} {:s}".format("Username", "Added Date", "Email"))
for (userame, added_date, email) in users:
    print("{:16s} {:28s} {:s}".format(userame, str(added_date), email))
print("================================================================\n")


### update movie description
query = "update video set description = %s where id = %s"
session.execute(query, ["Macbook 16'' Review: A Programmer Perspective", 11])
videos = session.execute("select author, name, description from video")
print("================================================================")
print("Videos Table")
print("{:16s} {:20s} {:s}".format("Author", "Name", "Description"))
for (author, name, description) in videos:
    print("{:16s} {:20s} {:s}".format(author, name, description))
print("================================================================\n")


## deletes

### delete event of mota in video 2
query = "delete from event where author = %s and video_id = %s"
session.execute(query, ["mota", 1])
events = session.execute("select * from event")
print("================================================================")
print("Events Table")
print(
    "{:<10s} {:13s} {:20s} {:20s} {:s}".format(
        "Video ID", "Author", "Moment", "Added Date", "Type"
    )
)
for (video_id, author, moment, added_date, _type) in events:
    print(
        "{:<10d} {:13s} {:20s} {:20s} {:s}".format(
            video_id, author, str(moment), str(added_date), _type
        )
    )
print("================================================================\n")


# alinea (b)

## (1) Os últimos 3 comentários introduzidos para um vídeo
query = "select * from comment_video_time where video_id = %s limit 3"
future = session.execute_async(query, [1])
try:
    print("================================================================")
    print(
        "{:<13s} {:20s} {:6s} {:s}".format("Video ID", "Author", "Name", "Description")
    )
    for (video_id, added_date, author, commment_text) in future.result():
        print(
            "{:<13d} {:20s} {:6s} {:s}".format(
                video_id, str(added_date), author, commment_text
            )
        )
    print("================================================================\n")
except ReadTimeout:
    print("Query timed out:")

## (3) Todos os vídeos com a tag Aveiro
query = "select videos from tag_video where tag = %s"
future = session.execute_async(query, ["trailer"])
try:
    print("================================================================")
    videos = future.result().one()
    print(videos.videos)
    print("================================================================\n")
except ReadTimeout:
    print("Query timed out:")

## (4) Os últimos 5 eventos de determinado vídeo realizados por um utilizador
query = "select * from event where video_id = %s and author = %s limit 5"
future = session.execute_async(query, [1, "ds"])
try:
    print("================================================================")
    print(
        "{:<9s} {:7s} {:20s} {:20s} {:s}".format(
            "Video ID", "Author", "Moment", "Added Date", "Type"
        )
    )
    for (video_id, author, moment, added_date, _type) in future.result():
        print(
            "{:<9d} {:7s} {:20s} {:20s} {:s}".format(
                video_id, author, str(moment), str(added_date), _type
            )
        )
    print("================================================================\n")
except ReadTimeout:
    print("Query timed out:")

## (5) Vídeos partilhados por determinado utilizador num determinado período de tempo
query = "select * from author_video where author = %s and added_date = %s"
future = session.execute_async(query, ["vascoalramos", "2019-11-21"])
try:
    print("================================================================")
    (
        author,
        added_date,
        count_rating,
        description,
        followers,
        _id,
        name,
        tag,
        total_rating,
    ) = future.result().one()
    print(f"{author}  |  {added_date}  |  {count_rating}  |  {description}  |  {followers}  |  {_id}  |  {name}  |  {tag}  |  {total_rating}")
    print("================================================================\n")
except ReadTimeout:
    print("Query timed out:")
