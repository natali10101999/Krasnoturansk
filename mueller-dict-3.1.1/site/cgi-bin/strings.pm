package strings;

use Encode;
use Exporter 'import';

@EXPORT = qw(get_str get_array);

$enc = 'koi8-r';

%title = (
	en => "V. K. Mueller English-Russian Dictionary",
	ru => "�. �. ������ �����-������� �������"
);

%prompt = (
	en => "Enter word:",
	ru => "������� �����:"
);

%label_submit = (
	en => "Search",
	ru => "������"
);

%label_checkbox_spell = (
	en => " Spelling correction",
	ru => " ��������� ������"
);

%label_checkbox_ipa = (
	en => " IPA symbols in transcription",
	ru => " ������� IPA � ������������"
);

%label_checkbox_scroll = (
	en => " Scroll to result",
	ru => " ���������� ���������"
);

%table_caption = (
	en => "Select database:",
	ru => "�������� ���� ������:"
);

%msg1 = (
	en => " %d definition%s found:",
	ru => " ������� %d ����������%s:"
);

%msg2 = (
	en => "[%d comparison%s]",
	ru => "[%d ��������%s]"
);

%msg3 = (
	en => "From",
	ru => "��"
);

%msg4 = (
	en => "No definitions found for <b>&quot;%s&quot;</b>",
	ru => "��� <b>&quot;%s&quot;</b> ���������� �� �������"
);

%msg5 = (
	en => ", perhaps you mean:",
	ru => ", ��������, �� ����� �����:"
);

%msg6 = (en=>"Go to top", ru=>"������");

%msg7 = (
	en => "Go to definitions",
	ru => "� ������������"
);

%headers = (
	en => ["Name",
		"Description",
		"Data size",
		"Index size",
		"Entries",
		"Version"],
	ru => ["��������",
		"��������",
		"������ ������",
		"������ ������-�����",
		"����",
		"������"]
);

%note = (
	en => "* Click on the link to learn more about selected database.",
	ru => "* �������� �� ������ ��� ��������� ����� ��������� ���������� � ��������� ���� ������."
);

%update_msg = (
	en => "Dictionary databases temporary unavailable.",
	ru => "���� ������ ������� �������� ����������."
);

%help = (
	en => "Click with mouse on phonetic transcription in square brackets to activate speech synthesizer.",
	ru => "�������� ������ �� ������������ ������������ � ���������� ������� ��� ��������� �������� �����������."
);

%report = (
	en => "Comment",
	ru => "�����������"
);

sub get_str {
	my($name,$lang) = @_;
	$lang = lc($lang);
	return exists(${$name}{$lang}) ? decode($enc,${$name}{$lang}) : ${$name}{'en'};

}

sub get_array {
	my($name,$lang) = @_;
	$lang = lc($lang);
	my $a = exists(${$name}{$lang}) ? ${$name}{$lang} : ${$name}{'en'};

	$_ = decode($enc,$_) foreach(@$a);
	return $a;
}

1;
