package strings;

use Encode;
use Exporter 'import';

@EXPORT = qw(get_str get_array);

$enc = 'koi8-r';

%title = (
	en => "V. K. Mueller English-Russian Dictionary",
	ru => "В. К. Мюллер Англо-Русский Словарь"
);

%prompt = (
	en => "Enter word:",
	ru => "Введите слово:"
);

%label_submit = (
	en => "Search",
	ru => "Искать"
);

%label_checkbox_spell = (
	en => " Spelling correction",
	ru => " Коррекция ошибок"
);

%label_checkbox_ipa = (
	en => " IPA symbols in transcription",
	ru => " Символы IPA в транскрипции"
);

%label_checkbox_scroll = (
	en => " Scroll to result",
	ru => " Показывать результат"
);

%table_caption = (
	en => "Select database:",
	ru => "Выберите базу данных:"
);

%msg1 = (
	en => " %d definition%s found:",
	ru => " Найдено %d определени%s:"
);

%msg2 = (
	en => "[%d comparison%s]",
	ru => "[%d сравнени%s]"
);

%msg3 = (
	en => "From",
	ru => "Из"
);

%msg4 = (
	en => "No definitions found for <b>&quot;%s&quot;</b>",
	ru => "Для <b>&quot;%s&quot;</b> совпадений не найдено"
);

%msg5 = (
	en => ", perhaps you mean:",
	ru => ", возможно, вы имели ввиду:"
);

%msg6 = (en=>"Go to top", ru=>"Наверх");

%msg7 = (
	en => "Go to definitions",
	ru => "К определениям"
);

%headers = (
	en => ["Name",
		"Description",
		"Data size",
		"Index size",
		"Entries",
		"Version"],
	ru => ["Название",
		"Описание",
		"Размер данных",
		"Размер индекс-файла",
		"Слов",
		"Версия"]
);

%note = (
	en => "* Click on the link to learn more about selected database.",
	ru => "* Щелкните на ссылке для получения более подробной информации о выбранной базе данных."
);

%update_msg = (
	en => "Dictionary databases temporary unavailable.",
	ru => "Базы данных словаря временно недоступны."
);

%help = (
	en => "Click with mouse on phonetic transcription in square brackets to activate speech synthesizer.",
	ru => "Щелкните мышкой на фонетической транскрипции в квадратных скобках для активации речевого синтезатора."
);

%report = (
	en => "Comment",
	ru => "Комментарий"
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
