import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

link = "postgres://iaduovpmoevsrt:8225056ab265e9a1818951bbc9ce12c730b1b47adf319afae2b41e7f1360c63d@ec2-54-235-193-0.compute-1.amazonaws.com:5432/de3f75hci6d3hk" 

engine = create_engine(link)
db = scoped_session(sessionmaker(bind=engine))


def main():
   fopen = open("books.csv")

   reader = csv.reader(fopen)

   for isbn,tit,auth,yr in reader:
        db.execute("INSERT INTO books (title,author,isbn,year) VALUES (:title,:author,:isbn,:year)",{"title":tit,"author":auth,"isbn":isbn,"year":yr})
        db.commit()
        print tit , auth , isbn , yr


if __name__ == "__main__":
  main()
  
