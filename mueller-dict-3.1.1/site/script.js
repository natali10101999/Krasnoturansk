function on_submit() {
	with(document.form) {
		if(!word.value.length) {
			word.focus();
			return false;
		}
	}
	return true;
}

function form_show() {
	document.location.hash = "a";
	setTimeout("with(document.form.word){select();focus();}", 500);
	return false;
}
