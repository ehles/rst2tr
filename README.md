# doc2tr

Converts test documentation to TestRail test cases


## Documentation schemas

### Classic schema
```

title
section
block_quote
enumerated_list
list_item
paragraph


document
    title
        Text
    section
        title
            Text
    section
        title
            Text
    section
        title
            Text
    
        block_quote
            enumerated_list
                list_item		
                    paragraph
                        Text
                list_item
```
Where sections are 
1. Test case title
2. Test case ID
3. Test case description
4. Test case complexity
5. Test case steps
6. Test case expected results

### Modern schema
```
here
```
