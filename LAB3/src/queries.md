Task 4.3Group by
```sql
SELECT COUNT(BookType.id), BookType.type
FROM BookType
group by BookType.type
```

Task 4.2 + 4.4 
```sql
USE Library; 
CREATE VIEW bookInfo As -- create view
SELECT *
FROM Book
JOIN BookType ON  BookType.bookId = Book.id;

SELECT name, author, edition, type
from bookInfo;
DROP view bookInfo;
```

get borrowed book base on personNum
```sql
USE Library;
Select bkId
From LoanDetails
JOIN Member ON LoanDetails.memberId = Member.id
WHERE personalNum = '34234545';
```