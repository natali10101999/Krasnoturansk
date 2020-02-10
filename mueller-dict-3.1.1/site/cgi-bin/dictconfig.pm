#
# user editable variables for dict.cgi
#

package config;

# full server-side path to data directory
$data_path = '/home/chg/dict/';

# full server-side and virtual path or url to images directory
$images_path = '/home/chg/public_html/dict/images';
$images = 'http://localhost/~chg/dict/images/';

# url or virtual path/name of external CSS file
$css = 'http://localhost/~chg/dict/style.css';

# show top menu (select charset) even if we can provide requested charset
$sticky_top_menu = 1;  # boolean

# colorize article body
$colorize = 1;

# create file with this name in data directory for temporary lock access
$lock_file = '.lock';

# full server-side path/name of file with banner code (comment to disable)
#$banner = '/home/chg/banner';

# speech senthesizer request string (comment to disable)
# passed parameters:
#  %1 - phrase or transcription in square brackets
$say = "/cgi/say.cgi?s=%s";

# bug reporter request string (comment to disable)
# passed parameters:
#  %1 - database name
#  %2 - database version
#  %3 - article headword
$report = "mailto:smersh\@users.sourceforge.net?subject=mueller-dict&body=Database: %s v%s%%0aHeadword: %s%%0a%%0aEnter your comments here...";

do('overconf');

1;
