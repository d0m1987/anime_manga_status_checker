# Development

## General class structure
Thinking about the generall class structure, I came up with the following UML diagram: 
![alt text][uml_diagram]

The idea behind each class is briefly explained in the following paragraphs.

### User
The `User` class holds information about WHAT the user wants to be informed about (read: the homepages he is interested in) and HOW to contact the user. To be notified about homepage updates, the `User` class implements the `HomepageUpdateInterface`.  
The attribute `homepages` has two use cases:
- The keys are the homepages the user wants to be informed about.
- The values (list of episodes) hold the information about new episodes.
First, I had these two points in two attributes but it seems to me, that this solution is more elegant. If we have both information separated, e.g. like here
```python
class User:
    homepages: List[Homepage] = list()
    updates_to_be_notified: List[Tuple[Homepage, Episode]] = list()
```

we need to delete the homepage in the attribute homepages AND in the attribute updates_to_be_notified if the user wants to be unassigned.
Furthermore, the above code holds references to the homepage objects more than once. This might not be a big deal in our case, but I think it's noteworthy. 

### Homepage
The `Homepage` class has two major functions:
- be the source for episode parsers that know how to create episodes from the homepage
- know how to create information from episodes (i.e. identify updates) and make these public to the users that have registered for updates.

The latter one is realized with the Pub-Sub or Observer pattern (see e.g. [Observer Pattern article](https://refactoring.guru/design-patterns/observer)). Every class that implements the HomepageUpdateInterface would generally be able to receive updates from the `Homepage` class if an update occured.

The class attribute `Homepage.homepages` is used to keep track which homepages are currently available to register for. 

### EpisodeParser
The `EpisodeParser` itself is only an abstract class. As we've seen during our analysis, the structure of the pages HTML can be totally different and require different approaches to get the episode data.
Thus, we are only declaring an interface that each concretization of an episode parser needs to implement.  
The class attribute `EpisodeParser.episode_parsers` is used to keep track of all concrete implementations of `EpisodeParser` in an automated, structured way. The hook function `__init_subclass__` in the `EpisodeParser` allows us to automatically register concrete implementations.

### Episode
The `Episode` class is more or less only a data container for episode information. The only special about it is, that we are overwriting the dunder `__gt__` method, such that we can easily compare episodes against each other, e.g. to identify the newest one.

## Implementing the class structure (only the shell without function)

Based on the thoughts above, I implemented a basic file / module structure as follows:

```bash
html_update_checker
├── episode.py
├── episode_parser_implementations
│   ├── __init__.py
│   ├── dragonball_super_anime.py
│   └── one_piece_anime.py
├── homepage.py
└── user.py
```

In my opinion, this should be sufficient for a first step.

During the implementation I encountered circular imports because of type annotations, e.g. between `User` and `Homepage`. I solved them by using the Python Enhancement Proposal (PEP) 484, i.e. quoting the types -> [Forward reference to solve circular type checks](https://www.python.org/dev/peps/pep-0484/#forward-references)

With this implementation, we are now ready to do the real implementation :-)

## Implementation approach: Test driven development (TDD)

Since some time I'm really into the idea of using TDD for my programming and with this program, I'd like to try this approach. A super good base for my learning was the article [Modern Test-Driven Development in Python
](https://testdriven.io/blog/modern-tdd/) by Jan Giacomelli. I can really recommend it!

## Technology / programming techniques / libraries I plan to use

I already mentioned some techniques (Observer pattern), technologies (Raspberry Pi, Docker) and implicitly libraries (pytest via the TDD article) I'd like to use. To make it more concrete, here a complete list that will be updated step by step.

Technology:
- Raspberry Pi
- Virtual private server (VPS) from [Contabo](https://contabo.de/?show=vps)
- Docker / Docker Compose

Programming techniques:
- Observer pattern

Libraries:
- requests (for HTTP requests)
- funcy (provides a great retry decorator)

## Getting the setup up and running

To get the setup up and running (and to have spare time for new projects), I'm going to reduce the project to the minimum such that it works.

I have a lot of other ideas, e.g.
- Split the codebase into 1) Crawler and 2) User with update functionalities
- Prepare the code to be split into microservices, such that I can e.g. spin up additional services if there are a lot of pages to scrape.
- Generalize the code more, e.g. a dictionary with attributes instead of the concrete `name`, `url` and `episode_number`.

But thinking about the time I would need to implement all of that (and having in mind that I do not have a MVP yet), I'll go and get it up running on my Raspberry Pi asap.

## Generalizing the episode parser implementations
As we've seen in the [analysis](./docs/analysis/analysis_anime_pages.md#analyse-the-pages-you-would-like-to-scrape), nearly all pages can be parsed using the css class selector "mediaitem". Only for the One Piece Manga, we need to use the css class selector "sagatable". Thus, I reorganized the episode_parser_implementations to only contain these two parsers instead of having a separate parser for each homepage.

## Exception handling
To see which excdeptions occur during runtime, I wrapped the `schedule.run_pending()` in a try... except block. All exceptions are catched and printed.  
The plan is to add exception handling iteratively, since this is a hobby project and no other system / person depends on this system running (except for me, waiting for the next episodes :yum:).

## Updating start.py
I included now all homepages to `start.py`.  
First tries showed, that the pickled Gmail token somehow expired. So I'm thinking about building `gmail.py` again or even switching to [Sendgrid](https://sendgrid.com/pricing/), since they offer 100 mails / day for free.  
When this is done, I'll let the program run for a day or so on my working machine. If this runs properly, I'll push it to my Raspberry Pi.

## Running the script on my Raspberry Pi
The script is now running locally on my Raspberry Pi. It's run in an endless loop with the library `schedule` from Dan Bader and started automatically with crontab at startup.  
The concrete command can be found in the [ReadMe](.ReadMe.md)

[uml_diagram]: ./img/uml.png "UML diagram for the program"