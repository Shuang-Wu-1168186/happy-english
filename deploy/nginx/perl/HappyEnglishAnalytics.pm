package HappyEnglishAnalytics;

use nginx;

# This handler deliberately does not interpret or persist event data.  It
# asks Nginx to read the request body and returns a small acknowledgement; the
# `happy_analytics_json` access log writes the body after this callback.
sub handler {
    my $r = shift;

    if ($r->request_method ne 'POST') {
        $r->discard_request_body;
        return HTTP_NOT_ALLOWED;
    }

    return $r->has_request_body(\&acknowledge) ? OK : HTTP_BAD_REQUEST;
}

sub acknowledge {
    my $r = shift;

    $r->status(202);
    $r->send_http_header('application/json; charset=utf-8');
    $r->print('{"accepted":true}');
    return OK;
}

1;
