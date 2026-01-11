## 2026-01-06

I'm starting the implementation of PAM with the example from chapter 14. First step: implement FIND-OUT-REQ: based on the sentence "John was lost", the system deducts that John will want to find out where he is. That is: a goal deduction rule.

## 2026-01-01

I asked Gemini for help on whom to contact for the original PAM source code. It suggested Christopher Riesbeck, one of the earliest members of the group around Shank. So I emailed him to help me find the source code. He responded by saying he didn't have any code left from that era, and that he'd also asked around. This means that I will have to re-invent the rules used to describe all domain knowledge, but at least I know that the code is not just accessible in an easy to find place. Riesbeck is also a coauthor of the book "Inside Computer Understanding: Five Programs Plus Miniatures", which contains a "micro implementation" of a.o. the PAM program. I ordered it from Amazon.

As input for PAM is complete stories, and yet they are processed one line at a time, I need the parser to be able to return multiple parse trees for a single piece of text. The parse trees it returned before are ambiguous variants. Each of these variants will now consist of multiple trees.
