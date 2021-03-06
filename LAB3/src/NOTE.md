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

DROP VIEW bookStock
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

members that have borrowed the most books
``` sql
Use Library;
Select concat(firstName, ' ', lastName) as MemberName, count(memID) as numberOfLaons
from Member
JOIN loanDetails on loanDetails.member_id = Member.memID
GROUP BY MemberName
HAVING numberOfLaons > 0
ORDER BY numberOfLaons DEsC

```
books that have borrowed the most books
``` sql
Use Library;
Select name as BookName,author as bookAuthor, type as bookeType, edition as bookEd ,count(bkID) as numberOfLaons
from Book
JOIN LoanDetails on LoanDetails.book_id = Book.bkID
GROUP BY BookName,bookAuthor, bookeType,bookEd
HAVING numberOfLaons > 0
ORDER BY numberOfLaons DEsC

```
get borrowed book info based on a giver personNum
``` sql
select *
From Book
where bkID in(
    SELECT book_id
    From LoanDetails
    JOIN `Member` ON LoanDetails.member_id = Member.memID
    WHERE personalNum = '1111');
)

```

delete and ignore FK constrain problem 
```sql
SET FOREIGN_KEY_CHECKS = 0;
truncate table `Member`;
SET FOREIGN_KEY_CHECKS = 1;
```

# book type
1.  Children's 
2.  Drama 
3.   Fantasy 
4.    Horror 
5.     Romance
6.      Science fiction 
7.       Biography 
8.       ETC

## video
- show everything
- add delete member
- add book
- borrow a book 
- return a book
- check expried book by date
- best reader
- best book
- get borrowed book