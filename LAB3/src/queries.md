Task 4.3Group by
```sql
SELECT COUNT(BookType.id), BookType.type
FROM BookType
group by BookType.type
```

Task 4.2 + 4.4 
```sql
USE Library;
CREATE VIEW bookStock As -- create view
select * 
from Book
join Stock on Book.bkID = Stock.book_id;
```

get amount of bookStock
```sql
USE Library;
select amount
from bookStock
where name = 'the lord of underwear' and edition = '1';
```

get borrowed book base on personNum
```sql
USE Library;
Select bkId
From LoanDetails
JOIN Member ON LoanDetails.memberId = Member.id
WHERE personalNum = '34234545';
```