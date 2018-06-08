# AtomicKotlin-hugo
Hugo Static Site sources for the book website

Because of the theme, the site automatically works well on phones as well as
computers and tablets.

Everything is in markdown so it's very easy to add/edit content. If you look
at the "content" subdirectory you'll see how straightforward it is to add new
pages.

## To Build:

1.  [Install the Hugo](https://hugodocs.info/getting-started/installing/#quick-install) static site generator.

2.  Clone this repository into your "git" subdirectory.

3.  From within this repository, run `hugo server` and open your browser at the URL given.

4.  To create the deployable version, run `hugo` from within this repository.
    You should now see a `public` directory, which contains the deployable file
    set.

5.  To duplicate what happens during an actual deploy, first clone
    [AtomicKotlin.github.io](https://github.com/AtomicKotlin/AtomicKotlin.github.io)
    into your "git" subdirectory. Now run `python deploy.py` from within this
    subdirectory.

