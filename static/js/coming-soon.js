function error500Message() {
	errorMessage('Something went wrong and our support team was notified. Please try again later.')
}

function urlNotFound() {
	errorMessage("We couldn't find the a Shortenr URL with that slug. Double check and try again.")
}

function errorMessage(text) {
    new Noty({
      type: 'error',
      layout: 'topRight',
      killer: true,
      theme: 'nest',
      text: `<i class="fa fa-times fa-2x fa-pull-left" aria-hidden="true"></i><strong>Uh oh.</strong> ` + text
    }).show();
}