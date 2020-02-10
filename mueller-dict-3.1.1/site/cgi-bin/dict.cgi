#! /usr/bin/perl -w

############################################################################
# $Id: dict.cgi,v 1.3 2005/06/25 20:25:21 chg Exp $
# dict.cgi retrieves data from DICT-server compatible databases
#
# Some ideas was borrowed from the sourcecode of dictd (Rickard E. Faith).
#
# This program is free software.  You can redistribute it and/or modify
# it under the terms of the GNU General Public License
#
# http://sourceforge.net/projects/mueller-dict/
#
# Copyright (C) 2005 CHG <smersh@users.sourceforge.net>
#
# Created: Wed,  6 Apr 2005 23:43:54 +0500 CHG
# Changed: Wed, 05 Jul 2006 12:10:15 +0500 CHG
#
############################################################################

# !!!! THE LOCATION OF CONFIG. FILES !!!!
#use lib qw(/home/chg/src/dictcgi);

use CGI::Carp qw(fatalsToBrowser);
use 5.008_000;

use constant VERSION => '1.3.4';

use CGI qw(:standard :html3 -nosticky -no_xhtml *table center);
use File::Basename;
use integer;
use Encode;

use strings;  # translations
use dictconfig;  # user editable variables

$| = 1;
$CGI::POST_MAX=1;  # posted data limit in bytes
$CGI::DISABLE_UPLOADS = 1;  # no uploads
$arg_sep = ';';

$self_name = basename($0,'');

%ipa2img = (
	"a" => "41.gif",
	"ú" => "44.gif",
	"E" => "45.gif",
	"I" => "49.gif",
	"N" => "4e.gif",
	"ü" => "51.gif",
	"S" => "53.gif",
	"æ" => "54.gif",
	"Ú" => "5a.gif",
	"b" => "62.gif",
	"d" => "64.gif",
	"e" => "65.gif",
	"f" => "66.gif",
	"g" => "67.gif",
	"h" => "68.gif",
	"i" => "69.gif",
	"j" => "6a.gif",
	"k" => "6b.gif",
	"l" => "6c.gif",
	"m" => "6d.gif",
	"n" => "6e.gif",
	"o" => "bf.gif",
	"p" => "70.gif",
	"r" => "72.gif",
	"s" => "73.gif",
	"t" => "74.gif",
	"u" => "75.gif",
	"v" => "76.gif",
	"w" => "77.gif",
	"z" => "7a.gif",
	"O" => "8d.gif",
	"Ü" => "ab.gif",
	"A" => "c3.gif",
	"," => "c7.gif",
	"'" => "c8.gif",
	":" => "f9.gif"
);

%b64_index = (
	"A" => 0,   "R" => 17,  "i" => 34,  "z" => 51,
	"B" => 1,   "S" => 18,  "j" => 35,  "0" => 52,
	"C" => 2,   "T" => 19,  "k" => 36,  "1" => 53,
	"D" => 3,   "U" => 20,  "l" => 37,  "2" => 54,
	"E" => 4,   "V" => 21,  "m" => 38,  "3" => 55,
	"F" => 5,   "W" => 22,  "n" => 39,  "4" => 56,
	"G" => 6,   "X" => 23,  "o" => 40,  "5" => 57,
	"H" => 7,   "Y" => 24,  "p" => 41,  "6" => 58,
	"I" => 8,   "Z" => 25,  "q" => 42,  "7" => 59,
	"J" => 9,   "a" => 26,  "r" => 43,  "8" => 60,
	"K" => 10,  "b" => 27,  "s" => 44,  "9" => 61,
	"L" => 11,  "c" => 28,  "t" => 45,  "+" => 62,
	"M" => 12,  "d" => 29,  "u" => 46,  "/" => 63,
	"N" => 13,  "e" => 30,  "v" => 47,
	"O" => 14,  "f" => 31,  "w" => 48,
	"P" => 15,  "g" => 32,  "x" => 49,
	"Q" => 16,  "h" => 33,  "y" => 50,
);

$config::images .= '/' unless $config::images =~ m{/$};
$config::images_path .= '/' unless $config::images_path =~ m{/$};
$config::data_path .= '/' unless $config::data_path =~ m{/$};

# acceptable charsets in form;
#     label => [qw(canonical_name alias1 alias2 ...)]
# canonical_name must be presented in list returned by "piconv -l"
%charsets = (
	UNIX=>[qw(koi8-r)],
	Windows=>[qw(windows-1251 cp1251)],
	ISO=>[qw(iso-8859-5 ISO_8859-5:1988 GOST_19768 GOST_19768-74)],
	UTF=>[qw(utf8)],
	DOS=>[qw(cp866 ibm866)],
	Mac=>[qw(MacCyrillic x-mac-cyrillic)]
);

$def_charset = 'koi8-r';  # default charset of output pages

# available translations
@langs = qw(en ru);
$def_lang = 'en';

# list of acceptable CGI parameters
@params = qw(dict spell ipa scroll word charset lang q_enc);

$hash_ext = "hash";
$optimized_start = 1;
$max_word_length = 50;

# delete unknown parameters from query
LOOP: foreach $p (param()) {
	foreach(@params) {
		next LOOP if $p eq $_;
	}
	Delete($p);
}

# check CGI errors after first param() call
{
	my $error = cgi_error();
	croak($error) if $error;
}

param("scroll", "on") unless param();  # enable scroll by default

# get clients's preferred charset canonical name

if(defined(my $c=param("charset"))) {
	foreach $a (keys(%charsets)) {foreach(@{$charsets{$a}}) {
		$force_charset = $charsets{$a}[0], last if normalize($_) eq normalize($c);
	}}
}

$auto_charset = get_charset();

if(defined($force_charset)) {
	$charset = $force_charset;
} elsif(defined($auto_charset)) {
	$charset = $auto_charset;
} else {
	# choose charset by clients's platform name as last resort
	$charset = (user_agent() && (user_agent('win') || user_agent('msie'))) ?
		"windows-1251" : $def_charset;
}

binmode(STDOUT=>":encoding($charset)");
#binmode(STDIN=>":encoding($charset)");

# encoding of query
if(defined(my $q=param('q_enc'))) {
	foreach $a (keys(%charsets)) {foreach(@{$charsets{$a}}) {
		$q_enc = $charsets{$a}[0], last if normalize($_) eq normalize($q);
	}}
	Delete('q_enc');
}

# preprocess input word

if(defined($word = param("word"))) {
	Encode::from_to($word, (defined($q_enc)?$q_enc:$charset), 'utf-8');
	$word = decode_utf8($word);
	$word = substr($word, 0, $max_word_length);  #trancate
	$word = normalize($word, '\p{L}\p{Z}\p{Nd}');
	param("word", $word);
}

# get clients's preferred language

if(defined($_=param("lang"))) {
	foreach $l (@langs) {
		if(lc($_) eq lc($l)) {
			$force_lang = $l;
			last;
		}
	}
}
$auto_lang = get_lang();

if(defined($force_lang)) {
	$lang = $force_lang;
} elsif(defined($auto_lang)) {
	$lang = $auto_lang;
} else {
	# choose language by clients's browser localization as last resort
	$lang = (user_agent() && user_agent("[ru]")) ? "ru" : $def_lang;
}

$top = '' unless do 'dict-top';
$foot = '' unless do 'dict-foot';

# top menu

$top_menu = '';

if($config::sticky_top_menu || !defined($auto_charset)) {
	$top_menu = "<center>| ";

	$top_menu .= a({-href=>create_query(charset=>undef, q_enc=>normalize($charset)),
		-onclick=>"link_type='charset';override_link(event);return true;"},
		'Auto').' | '
	if defined($auto_charset) && ($auto_charset ne $charset);

	while(my($l, $a)=each(%charsets)) {
		if($$a[0] ne $charset) {
			$top_menu .= a({-href=>create_query(charset=>normalize($$a[0]),
				           q_enc=>normalize($charset)),
				-onclick=>"link_type='charset';override_link(event);return true;"}, $l);
		} else {
			$top_menu .= $l;
		}
		$top_menu .= " | ";
	}

	$top_menu .="</center>";
}

# warn and exit if data directory is locked
if(-e "${config::data_path}${config::lock_file}") {
	print(
		header(
			-expires=>'-1d',
			-charset=>$charset,
		),
		start_html(
			-head=>meta({-http_equiv=>'Content-Type',
				-content=>"text/html; charset=$charset"}),
			-title=>get_str('title',$lang),
			-style=>{-src=>$config::css},
		),
		$top_menu,
		$top,
		center({-class=>'msg'}, get_str('update_msg',$lang)),
		$foot,
		end_html(),
	);

	exit(0);
}

# enumerate available dictionaries
@dicts = @{initialize($config::data_path)};

# select dictionaries
{
	my $f = 0;

	if(param('dict')) {
		foreach $d (param("dict")) {
			foreach(@dicts) {
				if($_->{name} eq $d) {
					$f = $_->{selected} = 1;
					last;
				}
			}
		}
	}
	unless($f) {
		foreach(@dicts) {
			$f=$_->{selected}=1 if $_->{checked};
		}

	}
	unless($f) {
		$_->{selected} = 1 foreach @dicts;
	}
}

# regenerate 'dict' array
Delete('dict');
foreach(@dicts) {
	push(@{param_fetch('dict')}, $_->{name}) if $_->{selected};
}

# counters for statistics
$count_comps = 0;  # total number of comparisons 
$count_defs = 0;   # number of definitions found

$up_link = a({-href=>'#top', onclick=>"go_top();return false;"},
	img({-alt=>get_str('msg6',$lang), -align=>'right',
		-src=>"${config::images}up.gif", border=>"0",
		attr_gif_size("${config::images_path}up.gif")}
	)
);

$body = do_work($word);
$has_body = $body ne '';

$javascript = '' unless do 'dict-javascript';

$down_arrow_img = img({-alt=>get_str('msg7',$lang), -align=>'right',
	-src=>"${config::images}down.gif", border=>"0",
	attr_gif_size("${config::images_path}down.gif")}
);

print(
	header(
		-expires=>'+1d',
		-charset=>$charset
	),
	start_html(
		-head=>meta({-http_equiv=>'Content-Type',
			-content=>"text/html; charset=$charset"}),
		-meta=>{description=>$strings::title{en}},
		-title=>get_str('title',$lang),
		-style=>{-src=>$config::css},
		-script=>$javascript,
		-onload=>'on_load();',
	),
	(defined($config::banner) && open($config::banner, $config::banner)) ?
		center(<$config::banner>).br : '',
	defined($top_menu) ? $top_menu : '',
	$top,
	($has_body ? a({-href=>'#defs', -name=>'top'}, $down_arrow_img) : ''),
	create_form(),
	($has_body ? a({name=>'defs'}, hr({-noshade=>undef, -size=>1})) : ''),
	$body,
	($has_body ? $up_link : ''),
	$foot,
	end_html(),
);

exit(0);


sub do_work {
	my $word = shift;

	return '' unless param("dict") && defined($word) && $word ne '';

	my $body;

	foreach $dict (@dicts) {
		next unless($dict->{selected});

		foreach(search_exact($dict, $word)) {
			next unless my ($headword, $offset, $length)=(split_index($_));

			$count_defs++;

			seek(\*{$dict->{data}}, b64_decode($offset), 0);
			read(\*{$dict->{data}}, my $data, b64_decode($length));
			$data = escapeHTML(decode($dict->{enc}, $data));
			colorize($data) if $config::colorize;
			$data =~ s/(\[)(.+?)(\])/$1.replace_phonet($2).$3/ge;
			$data = pre({-class=>'article'}, $data);
			$data .= div({-class=>'rep'}, a({-target=>'report_window',
				-href=>sprintf($config::report, $dict->{name}, $dict->{version},
					encode_url($headword))},
				img({-border=>0, -src=>$config::images.'note.gif', -align=>'bottom',
					attr_gif_size($config::images_path.'note.gif'), -alt=>''}
				).'&nbsp;'.get_str('report',$lang)
			)) if defined($config::report);

			$body .= $up_link.hr({-noshade=>undef, -size=>1}).
			table({-width=>'100%', -cellpadding=>3, -cellspacing=>0, -border=>0},
				Tr(th({-class=>'hdr'}, get_str('msg3',$lang), $dict->{desc}, "[$dict->{name}]:")),
				Tr(td({-class=>'tbl'}, $data))
			);
		}
	}

	if($count_defs) {
		$body = span({-class=>'msg'},
			sprintf(get_str('msg1',$lang), $count_defs, suffix($count_defs, $lang))
		).br.$body;
	} else {
		$body = span({-class=>'msg'}, sprintf(get_str('msg4',$lang), escapeHTML($word)));

		if(($_=param("spell")) && /^on$/i) {
			my $f = 0;

			foreach $dict (@dicts) {
				next unless($dict->{selected});

				my @result = search_levenshtein($dict, $word);
				if(@result) {
					$body .= span({-class=>'msg'}, get_str('msg5',$lang))
						unless($f++);

					$body .= hr({-noshade=>undef, -size=>1}).b({-class=>'prompt'}, "$dict->{name}: ");

					foreach(@result) {
						next unless my ($match) = split_index($_);

						$body .= a({-href=>create_query(word=>$match, dict=>$dict->{name}),
							-target=>'dict_window'}, escapeHTML($match)).', ';
					}

					$body = substr($body, 0, -2);
				}
			}
		}
	}

	return $body .= br.i(sprintf(get_str('msg2',$lang), $count_comps, suffix($count_comps, $lang)));
}

sub create_form {
	my $form = 
		start_form(-method=>'get',
			-action=>$self_name,
			-name=>'form',
			-onsubmit=>'return check_form();',
		).
		table({-border=>0, -cellpadding=>10, -cellspacing=>0, -width=>'100%'},
			Tr(td({-nowrap=>undef, -valign=>'middle', -align=>'center'},
				b({-class=>'prompt'}, get_str('prompt',$lang)),
				textfield(
					-name=>"word",
					-size=>50,
					-maxlength=>$max_word_length,
					-id=>'textfield',
				),
				submit(
					-name=>'submit',
					-value=>get_str('label_submit',$lang),
					-id=>'button'
				),
			))
		).
		table({-border=>0, -cellpadding=>10, -cellspacing=>0, -width=>'100%'},
			Tr({-valign=>'top', -align=>'center'}, td([
				checkbox(
					-name=>"spell",
					-value=>"on",
					-label=>get_str('label_checkbox_spell',$lang),
				),
				checkbox(
					-name=>"ipa",
					-value=>"on",
					-label=>get_str('label_checkbox_ipa',$lang),
				),
				checkbox(
					-name=>"scroll",
					#-checked=>"checked",
					-value=>"on",
					-label=>get_str('label_checkbox_scroll',$lang),
				),
			]))
		).
		start_table({-border=>0, -cellpadding=>5, -cellspacing=>2, -width=>'100%'}).
		caption(b({-class=>'prompt'}, get_str('table_caption',$lang))).
		Tr({-valign=>"middle"},
			th({-class=>'hdr'}, [
				'&nbsp;',
				@{get_array('headers',$lang)},
			])
		);

	foreach $dict (@dicts) {
		$form .= Tr({-class=>'tbl', -valign=>"middle"},
			td({-align=>'center'},
				checkbox(
					-name=>"dict",
					-value=>$dict->{name},
					-checked=>"checked",
					-label=>'',
				),
			),
			td({-align=>'left', -nowrap=>undef},
				a({-href=>$self_name."?word=00-database-info${arg_sep}dict=$dict->{name}${arg_sep}scroll=on",
				   -target=>'dict_window'}, $dict->{name}), '*',
			),
			td({-align=>'left'},
				$dict->{desc},
			),
			td({-align=>'right', -nowrap=>undef}, [
				format_size($dict->{data_size}),
				format_size($dict->{index_size}),
				$dict->{entries},
				$dict->{version},
			]),
		);
	};

	$form .= end_table.small({-class=>'note'}, get_str('note',$lang));

	$form .= hidden(-name=>'lang', -default=>$lang) if defined $force_lang;
	$form .= hidden(-name=>'charset', -default=>$charset) if defined $force_charset;

	return $form.endform;
}

#
# convert base64 encoded string into integer
#
# Value Encoding  Value Encoding  Value Encoding  Value Encoding
#     0 A            17 R            34 i            51 z
#     1 B            18 S            35 j            52 0
#     2 C            19 T            36 k            53 1
#     3 D            20 U            37 l            54 2
#     4 E            21 V            38 m            55 3
#     5 F            22 W            39 n            56 4
#     6 G            23 X            40 o            57 5
#     7 H            24 Y            41 p            58 6
#     8 I            25 Z            42 q            59 7
#     9 J            26 a            43 r            60 8
#    10 K            27 b            44 s            61 9
#    11 L            28 c            45 t            62 +
#    12 M            29 d            46 u            63 /
#    13 N            30 e            47 v
#    14 O            31 f            48 w         (pad) =
#    15 P            32 g            49 x
#    16 Q            33 h            50 y
#
sub b64_decode {
	my @val = split(//, shift);

	croak("b64_decode: undefined argument") unless @val;

	my ($offset, $result) = (0, 0);

	foreach $c (reverse(@val)) {
		if(exists($b64_index{$c})) {
			$result |= $b64_index{$c} << $offset;
			$offset += 6;
		} else {
			croak("b64_decode: illegal character in base64 value");
		}
	}
	return $result;
}

sub search_exact {
	my ($dict, $word) = @_;

	my($start, $end) = offset_range($dict, $word);
	$start = search_binary($dict, $word, $start, $end);
	return search_linear($dict, $word, $start, $end);
}

sub search_binary {
	my ($dict, $word, $start, $end) = @_;

	croak("search_binary: one or more arguments are undefined")
		unless defined($word) && defined($start) && defined($end);

	return $start if $start >= $end;

	my $fd = \*{$dict->{index}};
	my $pos = ($start+$end)/2;
	my $old = '';

	while($pos > $start && $pos < $end) {
		seek($fd, $pos, 0);

		<$fd> if $pos;  # insure that $pos points to BOL
		last unless defined($_ = decode($dict->{enc}, <$fd>)) && $_ ne $old;
		$old = $_;

		my ($headword) = split_index($_);
		unless(defined($headword)) {
			$pos = tell($fd);
			next;
		}

		$count_comps++;

		if($word gt normalize($headword, '\p{L}\p{Z}\p{Nd}'))
		{
			$start = tell($fd);
		} else {
			$end = $pos;
		}

		$pos = ($start+$end)/2;
	}

	return $start;
}

sub search_linear {
	my ($dict, $word, $start, $end) = @_;

	croak("search_linear: one or more arguments are undefined") unless
		defined($word) && defined($start) && defined($end);

	return () if $start >= $end;
	
	my $fd = \*{$dict->{index}};

	# insure that $start points to BOL
	$start-- if $start;
	seek($fd, $start, 0); 
	if($start) {
		<$fd> unless <$fd> =~ /^$/;
	}

	my @result = ();

	while(defined(my $entry=decode($dict->{enc}, <$fd>)) && tell($fd) <= $end) {
		next unless my ($headword) = split_index($entry);
		$headword = normalize($headword, '\p{L}\p{Z}\p{Nd}');

		$count_comps++;

		if($word eq $headword) {
			push @result, $entry;
		} elsif($word lt $headword) {last;}
	}

	return @result;
}

#
# enumerate all valid databases in given directory and return
# reference to array of hash references with following members:
#
#    {name}       - base name
#    {index}      - index filename and reference to preopened fd
#    {data}       - data filename and reference to preopened fd
#    {index_size} - size of index file
#    {data_size}  - size of data file
#    {entries}    - number of entries
#    {desc}       - short description
#    {hash}       - hash reference
#    {version}    - version/release
#    {selected}   - selected from query (boolean)
#    {alphabet}   - array reference
#    {enc}        - charset encoding
#    {checked}    - select by default (boolean)
#    {order}      - order in list
#
sub initialize {
	my $data_path = shift;
	my @dicts = ();

	$data_path .= '/' unless $data_path =~ m{/$};

	while(<${data_path}*.index>) {
		m{/([^/]+)\.index$};

		# defaults
		my %dict = (
			name     => escapeHTML($1),
			enc      => 'koi8-r',
			version  => '?',
			desc     => '?',
			entries  => '?',
			alphabet => [0..9, 'a'..'z', ' '],
			order    => 10,
			checked  => 1,
		);
		my ($offset, $length);

		$dict{index} = "${data_path}$dict{name}.index";
		$dict{data} = "${data_path}$dict{name}.dict";

		next unless -r $dict{index} && -r $dict{data};

		croak("initialize: cannot open index file '$dict{index}': $!")
			unless open($dict{index}, $dict{index});

		croak("initialize: cannot open data file '$dict{data}': $!")
			unless open($dict{data}, $dict{data});

		$dict{index_size} = (stat(\*{$dict{index}}))[7];
		croak("initialize: cannot stat (or corrupted) index file: $dict{index}")
			unless $dict{index_size};

		$dict{data_size} = (stat(\*{$dict{data}}))[7];
		croak("initialize: cannot stat (or corrupted) data file: $dict{data}")
			unless $dict{data_size};

		# charset encoding

		$dict{enc} = 'utf8' if defined((search_linear(\%dict, "00databaseutf8", 0, $dict{index_size}))[0]);

		# extract version

		if(defined($_=(search_linear(\%dict, "00databaseinfo", 0, $dict{index_size}))[0])) {
			($offset, $length) = (split_index($_))[1, 2];
			seek(\*{$dict{data}}, b64_decode($offset), 0);
			read(\*{$dict{data}}, $_, b64_decode($length));
			if(defined(decode($dict{enc}, $_)) && /\bversion\s+([\d.]*)\s/i) {
				$dict{version} = $1;
			}
		}

		# extract description

		if(defined($_=(search_linear(\%dict, "00databaseshort", 0, $dict{index_size}))[0])) {
			($offset, $length) = (split_index($_))[1, 2];
			seek(\*{$dict{data}}, b64_decode($offset), 0);
			read(\*{$dict{data}}, $_, b64_decode($length));
			if(defined($_ = decode($dict{enc}, $_))) {
				chomp;
				s/\s*00-?database-?short\s*//i;
				$dict{desc} = $_;
			}
		}

		# extract alphabet set

		if(defined($_=(search_linear(\%dict, "00databasealphabet", 0, $dict{index_size}))[0])) {
			($offset, $length) = (split_index($_))[1, 2];
			seek(\*{$dict{data}}, b64_decode($offset), 0);
			read(\*{$dict{data}}, $_, b64_decode($length));
			if(defined($_ = decode($dict{enc}, $_))) {
				chomp;
				$dict{alphabet} = [sort(split(//))];
			}
		}

		# here is the only place where we read optional .hash files.
		# extract number of entries and create hash table.

		if(open(HASH, "<:encoding($dict{enc})", "${data_path}$dict{name}.$hash_ext")) {
			my $re_pair = qr/^[ \t]*(.+?)[ \t]+(.+?)[ \t]*$/;

			while(<HASH>) {
				next unless my($name, $val) = /${re_pair}/;

				if($name=~/^words$/i) {$dict{entries}=$val if $val=~/^\d+$/;}
				elsif($name=~/^select$/i) {$dict{checked}=0 if !$val || $val=~/^(?:no|off)$/i;}
				elsif($name=~/^order$/i) {$dict{order} = $val if $val=~/^\d+$/;}
				elsif($optimized_start && $val=~/^\d+$/) {$dict{hash}{$name}=$val;}
			}

			close HASH;
		} else {
			#carp("initialize: cannot open '${data_path}$dict{name}.$hash_ext': $!");
			$optimized_start = 0;
		}

		push(@dicts, \%dict);
	}

	@dicts = sort {${$a}{order} <=> ${$b}{order}} (@dicts);
	return \@dicts;
}

sub search_levenshtein {
	my ($dict, $word) = @_;

	my $tmp;
	my %matchs = ();
	my @result = ();

	# deletions
	if(length($word) > 1) {
		foreach(0 .. (length($word)-1)) {
			substr($tmp=$word, $_, 1, '');
			$tmp =~ s/^\s*(.*?)\s*$/$1/;
			$matchs{$tmp} = '';
		}
	}

	# transpositions
	foreach(0 .. (length($word)-2)) {
		my @word = split(//, $word);
		$tmp = $word[$_];
		$word[$_] = $word[$_+1];
		$word[$_+1] = $tmp;
		$tmp = join('', @word);
		$tmp =~ s/^\s*(.*?)\s*$/$1/;
		$matchs{$tmp} = '';
	}

	# insertions
	foreach $i (0 .. (length($word))) {
		foreach(@{$dict->{alphabet}}) {
			$tmp = substr($word, 0, $i).$_.substr($word, $i);
			$tmp =~ s/^\s*(.*?)\s*$/$1/;
			$matchs{$tmp} = '';
		}
	}

	# insertions at the end (see insertions above)
	#foreach(@{$dict->{alphabet}}) {
	#	$tmp = $word.$_;
	#	$tmp =~ s/^\s*(.*?)\s*$/$1/;
	#	$matchs{$tmp} = '';
	#}

	# substitutions
	foreach $i (0 .. (length($word)-1)) {
		foreach(@{$dict->{alphabet}}) {
			substr($tmp=$word, $i, 1, $_);
			$tmp =~ s/^\s*(.*?)\s*$/$1/;
			$matchs{$tmp} = '' if $tmp ne '';
		}
	}

	my $begin;
	foreach $word (sort keys %matchs) {
		my($b, $end) = offset_range($dict, $word);
		$begin = $b unless $begin;

		$begin = search_binary($dict, $word, $begin, $end);
		push(@result, (search_linear($dict, $word, $begin, $end))[0]);
	}

	return @result;
}

sub format_size {
	no integer;

	my $size = shift;
	my $tmp;

	if(($tmp=$size/1048576) >= 1.0) {
		sprintf("%.3f", $tmp)."&nbsp;(Mb)";
	} elsif(($tmp=$size/1024) >= 1.0) {
		sprintf("%.3f", $tmp)."&nbsp;(Kb)";
	} else {
		$size." (b)";
	}
}

#
# convert each character in input string into html image tag
#
# phon.  koi8r  IPA   gif
# symbol code   code  file
#
# a      0x61   0x41  41.gif
# ú      0xfa   0x44  44.gif
# E      0x45   0x45  45.gif
# I      0x49   0x49  49.gif
# N      0x4e   0x4e  4e.gif
# ü      0xfc   0x51  51.gif
# S      0x53   0x53  53.gif
# æ      0xe6   0x54  54.gif
# Ú      0xda   0x5a  5a.gif
# b      0x62   0x62  62.gif
# d      0x64   0x64  64.gif
# e      0x65   0x65  65.gif
# f      0x66   0x66  66.gif
# g      0x67   0x67  67.gif
# h      0x68   0x68  68.gif
# i      0x69   0x69  69.gif
# j      0x6a   0x6a  6a.gif
# k      0x6b   0x6b  6b.gif
# l      0x6c   0x6c  bc.gif
# m      0x6d   0x6d  6d.gif
# n      0x6e   0x6e  6e.gif
# o      0x6f   0x6f  bf.gif
# p      0x70   0x70  70.gif
# r      0x72   0x72  72.gif
# s      0x73   0x73  73.gif
# t      0x74   0x74  74.gif
# u      0x75   0x75  75.gif
# v      0x76   0x76  76.gif
# w      0x77   0x77  77.gif
# z      0x7a   0x7a  7a.gif
# O      0x4f   0x8d  8d.gif
# Ü      0xdc   0xab  ab.gif
# A      0x41   0xc3  c3.gif
# ,      0x2c   0xc7  c7.gif
# '      0x27   0xc8  c8.gif
# :      0x3a   0xf9  f9.gif
#
sub phonet2img {
	my $str = shift;
	my $ret;

	foreach $c (split(//, $str)) {
		#my $img = exists($ipa2img{$c}) ? $ipa2img{$c} : undef;
		my $c_ind = encode('koi8r',$c);
		my $img = exists($ipa2img{$c_ind}) ? $ipa2img{$c_ind} : undef;
		$ret .= defined($img) ?
			img({
				-src=>$config::images.$img,
				attr_gif_size($config::images_path.$img),
				#-height=>16,
				#-width=>16,
				-align=>'middle',
				-border=>0,
				-alt=>$c,
			}) : '<font color="#ff0000">'.escapeHTML($c)."</font>";
	}

	return $ret;
}

sub get_charset {
	no integer;

	my $field = http('HTTP_ACCEPT_CHARSET');
	my %hash = defined($field) ? %{split_field($field)} : ();

	foreach(sort {$b <=> $a} keys %hash) {
		foreach $c (@{$hash{$_}}) {
			foreach $a (keys(%charsets)) {foreach(@{$charsets{$a}}) {
				return $charsets{$a}[0] if normalize($c) eq normalize($_);
			}}
		}
	}

	return undef;
}

sub split_field {
	my $field = shift;
	$field =~ s/[ \t]//g;

	my %hash = ();

	foreach (split(/,/, $field)) {
		next if (my($name, $qvalue) = split(/;/, $_)) > 2;
		next unless defined $name && ($name ne '*');

		if(defined($qvalue)) {  # rfc2068
			next unless ($qvalue) = ($qvalue=~/^q=(0(?:\.\d{0,3})?|1(?:\.0{0,3})?)$/);
		} else {
			$qvalue = 1.0;
		}

		$qvalue = sprintf('%.3f', $qvalue);

		push(@{$hash{$qvalue}}, $name);
	}
	return \%hash;
}

sub normalize {
	my($str, $alphabet) = @_;

	$str = lc($str);
	$alphabet = "0-9a-z " unless $alphabet;  # default charset

	$str =~ s/\p{Z}+/ /g;
	$str =~ s/[^${alphabet}]//g;
	$str =~ /^ *(.*?) *$/;

	return $1;
}

sub create_query {
	my %h = @_;
	my $res = $self_name.'?';

	foreach $p (@params) {
		if(exists($h{$p})) {
			if(ref($h{$p})) {
				foreach(@{$h{$p}}) {
					$res .= "$p=$_$arg_sep";
				}
			} elsif(defined($h{$p})) {
				$res .= "$p=$h{$p}$arg_sep";
			}
		} elsif(param($p)) {
			foreach (param($p)) {
				$res .= "$p=$_$arg_sep";
			}
		}
	}
		
	# delete trailing separator
	$res =~ s/(.*)[${arg_sep}?]$/$1/;

	return $res;
}

sub get_lang {
	no integer;

	my $field = http('HTTP_ACCEPT_LANGUAGE');
	my %hash = defined($field) ? %{split_field($field)} : ();

	foreach(sort {$b <=> $a} keys %hash) {
		foreach(@{$hash{$_}}) {
			foreach $l (@langs) {
				return $l if lc($_) eq lc($l);
			}
		}
	}

	return undef;
}

sub suffix {
	my ($num, $lang) = @_;

	my $last = substr($num, -1, 1);

	if(lc($lang) eq 'en') {
		return ($num > 1) ? 's':'';
	} elsif(lc($lang) eq 'ru') {
		my $s;
		if(($num>=11 && $num<=19) || ($last>=5 && $last<=9) || $last == 0) {
			$s = 'Ê';
		} elsif($last == 1) {
			$s = 'Å';
		} else {
			$s = 'Ñ';
		}
		return decode($strings::enc,$s);
	} else {
		carp("suffix: unknown language id: $lang");
		return '';
	}
}

sub offset_range {
	my ($dict, $word) = @_;
	my $begin = 0;
	my $end = $dict->{index_size};
	my $key = substr($word, 0, 1);
	my @alphabet = @{$dict->{alphabet}};

	if($optimized_start) {
		my $i = 0;

		while($i <= $#alphabet && $alphabet[$i] lt $key) {$i++;}
		$i-- if $alphabet[$i] gt $key;

		my $j = $i++;

		while($j >= 0) {
			if(exists($dict->{hash}{$alphabet[$j]})) {
				$begin = $dict->{hash}{$alphabet[$j]};
				last;
			}
			$j--;
		}

		while($i <= $#alphabet) {
			if(exists($dict->{hash}{$alphabet[$i]})) {
				$end = $dict->{hash}{$alphabet[$i]};
				last;
			}
			$i++;
		}
	}

	return ($begin, $end);
}

#
# split index entry
#
sub split_index {
	$index = shift;
	my @ret;

	unless((@ret = $index=~/^(.+?)\t(\S+?)\t(\S+)$/) == 3) {
		carp("split_index: illegal index entry: '$index'");
		return ();
	}

	return @ret;
}

sub gif_size {
	my $file = shift;
	my($id, $width, $height, $data);

	if(open($file, $file)) {
		return ($width, $height) if
			read($file, $data, 10) == 10 &&
			(($id, $width, $height)=unpack("a6vv", $data)) == 3 &&
			$id=~/^GIF8\d/;
	}

	return ();
}

sub attr_gif_size {
	$file = shift;
	my @size;

	return('-width', $size[0], '-height', $size[1])
		if (@size = gif_size($file)) == 2;

	return();
}

sub replace_phonet {
	my $phonet = shift;
	(my $raw = $phonet) =~ s/\&#(\d{2});/chr($1)/ge;  # unescape HTML

	$phonet = phonet2img($raw) if ($_=param("ipa")) && /^on$/i;

	return defined($config::say) ?
		a({-href=>sprintf($config::say, '['.encode_url($raw).']'),
			-class=>'phonet', -target=>'player_window'}, $phonet) :
		$phonet;
}

sub encode_url {
	$arg = shift;
	$arg =~ s/([^a-zA-Z0-9])/'%u'.sprintf('%04x', ord($1))/ge;
	return $arg;
}

sub colorize {
	my $data = \$_[0];

	# emphasize headword
	$$data =~ s/^(.*)/span({-class=>'headword'}, $1)/e;

	# transcriptions
	$$data =~ s/(\[.+?\])/span({-class=>'phonet'}, $1)/ge;

	# abbreviations
	$$data =~ s/\b_(\S*?\.)/span({-class=>'abbrev'}, $1)/eg;

	# 1st 2nd and 3rd level section numbers
	$$data =~ s{
		(  # $1
			\n\n[ \t]+
		)
		(  # $2
			[IVX]\{1,3\} | (?: \d\d? | [*\#] ) [.)]
		)
		(  # $3
			\s+
		)
	}
	{
		$1.span({-class=>'ord'}, $2).$3;
	}egx;
			#[IVX]{1,3} | \d{1,2} [.)] | [*\#] [.)]

	# 4th level section numbers
	$$data =~ s{([^-,]\s+)([ÁÂ×ÇÄÅ£ÖÚÊÉËÌÍÎÏÐÒÓÔÕÆÈÃÞÛÝßÙØÜÀÑ]\))(\s+)}
			   {$1.span({-class=>'ord'}, $2).$3}eg;

	# english text

	my $lat = qr/[a-zA-Z]/;
	my $esc = qr/&(?:\#39|quot);/;  # ord. of "'" = 39 (dec)

	$$data =~ s{
		(  # $1
			\s | [({] \s* | (?<=$lat\))\b
		)
		(  # $2
			(?:
				(?:  # ascii word
					#(?:$lat | $esc)
					(?:
						$lat | $esc | -(?=\s*$lat)
					)+
					| \d+ (?=\s+$lat)
				)
				[.,!?:]*
				(?:  # space between words
					\s+
				)?
			)+
		)
		(  # $3
			\s | \s* [)};] | \b(?=\($lat) |$
		)
	}
	{
		$1.span({-class=>'lat'}, $2).$3;
	}egxs;
}
__END__
