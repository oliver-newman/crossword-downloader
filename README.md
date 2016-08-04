# crossword-downloader

`python downloadPuz.py` downloads the latest available  New York Times crossword
puzzle in .puz format, and downloads all puzzles not already downloaded, 
creating a filesystem so that a given file, for example, `Aug0416.puz`,
is in the folder `crossword_archive_path>/2016/8/`. The base 
`<crossword_archive_path>` is set by running `python setup.py
<crossword_archive_path>`. Recommended for use with cron or a similar service,
such as [LaunchControl](http://www.soma-zone.com/), to enable automatic 
everyday downloads. Puzzles are released at 10 PM EST on weekdays and 7 PM EST
on weekends.

## Todos

- [ ] Check for "gaps" in crossword archive - the script currently only goes
      back in time, downloading crosswords, until it finds one for a given date,
      and then stops.
- [ ] Allow more customization
