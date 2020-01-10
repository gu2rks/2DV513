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

get member info who borrowed book that's about to expire
``` sql
Use Library;
Select *
From Member
JOIN LoanDetails on Member.memID = LoanDetails.member_id
where expireDate in (
	select expireDate
    from LoanDetails
	where expireDate = '2020-01-31'
    )
```

``` sql
USE Library;
Select count(memID)
FROM Member
JOIN LoanDetails on Member.memID = LoanDetails.member_id
Where book_id  in (
	select book_id
    from LoanDetails
    where book_id = 2
)
```