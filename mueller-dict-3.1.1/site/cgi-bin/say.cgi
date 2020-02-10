#! /usr/bin/perl -w
# $Id: say.cgi,v 1.2 2005/06/25 20:25:22 chg Exp $
#
# say.cgi: simple cgi frontend to rsynth speech syntesizer
#
# parameters:
#	s=<string>               - say the string
#	d=[a]merican|[b]ritish   - using accent dictionary
#
# created: Wed, 15 Jun 2005 13:20:01 +0500 CHG
#

use encoding 'koi8-r', STDIN=>undef, STDOUT=>undef;

$| = 1;
$dict = 'b';  # default accent dictionary

# full server-side pathname of rsynth executable
$rsynth = '/home/chg/src/rsynth-2.0/say';

$err1 = "Illegal query string";
$err2 = "Internal error";

%ipa2say = (
	'p'  => 'p',
	'b'  => 'b',
	't'  => 't',
	'd'  => 'd',
	'k'  => 'k',
	'm'  => 'm',
	'n'  => 'n',
	'l'  => 'l',
	'r'  => 'r',
	'f'  => 'f',
	'v'  => 'v',
	's'  => 's',
	'z'  => 'z',
	'h'  => 'h',
	'w'  => 'w',
	'g'  => 'g',
	'S'  => 'S',
	'N'  => 'N',
	'æ'  => 'T',
	'ú'  => 'D',
	'Ú'  => 'Z',
	'j'  => 'j',
	'I'  => 'I',
	'e'  => 'e',
	'i:' => 'i',
	'a:' => 'A',
	'O:' => 'O',
	'u:' => 'u',
	'Ü:' => '3R',
	'ü'  => '&',
	'A'  => 'V',
	'O'  => '0',
	'u'  => 'U',
	'Ü'  => '@',
	'OI' => 'oI',
	'E'  => 'e',
	'ou' => '@U',
	'a'  => 'a',
	"'"  => "'",
	','  => ','
);

error($err2) unless -x $rsynth;
error($err1) unless defined($_=$ENV{QUERY_STRING}) && /=/;

@pairs = split(/[&;]/);
foreach(@pairs) {
	my ($name, $value) = split(/=/, $_, 2);
	if($name eq 's') {$str = $value;}
	elsif($name eq 'd' && lc($value) eq 'a') {$dict = 'a';}
}
error($err1) unless defined($str) && $str ne '';

$str =~ s/%(?:([0-9a-fA-F]{2})|[uU]([0-9a-fA-F]{4}))/chr(hex(defined($1)?$1:$2))/ge;
$str =~ s/[-_+]/ /g;
$str =~ s/\s+/ /g;
$str = substr($str, 0, 100);
$str =~ s/(\[)(.*?)(\])/$1.ipa2say($2).$3/ge;
$str =~ s/(.)/($_=ord($1))>0x1f && $_<0x80 ? $1:''/ge;
error($err1) unless defined($str) && $str ne '';

print("Content-Type: audio/basic\n\n");
open(SAY, "|$rsynth -d $dict -a -o -") or die;
print SAY $str;

#
# report about error
#
sub error {
	my $msg = shift; $msg = '' unless defined($msg);
	my $date = localtime(time);
	my ($basename) = $0 =~ m{([^/]*)$};
	my $client = defined($ENV{REMOTE_ADDR}) ? $ENV{REMOTE_ADDR} : 'localhost';

	print STDERR "[$date] [error] [client $client] $basename: $msg\n";

	print <<END;
Content-Type: text/html

<html>
<head><title>Error</title></head>
<body>
[$date] [error] <b>$msg</b>
<hr><address>Maintained by <a href="mailto:smersh\@users.sourceforge.net">&lt;smersh\@users.sourceforge.net&gt;</a><br>
(insert signature <b>CHG</b> anywhere in Subject: field)</address>
</body>
</html>
END

	exit(0);
}

#
# convert transcription from ipa to rsynth notation
#
sub ipa2say {
	my $in = shift;
	my $l = length($in);
	my $i = 0;
	my $out = '';

	while($i < $l) {
		if(exists($ipa2say{my $t = substr($in, $i, 2)})) {
			$out .= $ipa2say{$t}; $i++;
		} elsif(exists($ipa2say{$t = substr($in, $i, 1)})) {
			$out .= $ipa2say{$t};
		}
		$i++;
	}
	return $out;
}
__END__
