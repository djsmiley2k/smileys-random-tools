use strict;
use warnings;

use Irssi;
my $VERSION = ("0.55");
my %IRSSI = (
	authors => 'djsmiley2k',
	contact => 'djsmiley2k@gmail.com',
	name => 'Old Channel',
	description => 'automatically splits out old channel window; closes older channel window and joins new channel',
	license => 'GPL2',
);

my ($curr_chan, $old_chan, $old_old_chan);
$curr_chan = Irssi::active_win->{refnum};
$old_old_chan = -1;

sub make_win {
        # Make new window using $old_chan
        # /window show $old_chan
        $old_chan = Irssi::active_win->{refnum};
	print "stored old chan value ($old_chan)";
}

sub push_old {
	$curr_chan = Irssi::active_win->{refnum};
	if ($old_old_chan != -1) {
		Irssi::command("/window show " . $old_chan);
		Irssi::command("/window hide " . $old_old_chan);
		print "old chan = $old_chan; curr_chan = $curr_chan; closing old_old_chan ($old_old_chan)";
	} else {
                Irssi::command("window show " . $old_chan);
		print "Nothing to close; old_chan = $old_chan; curr_chan = $curr_chan; old_old_chan = $old_old_chan";
		}
	$old_old_chan = $old_chan
}

Irssi::signal_add_first( 'window changed', \&make_win);
Irssi::signal_add_last( 'window changed', \&push_old);

### Irssi::signal_add_last( 'window changed', \&store_new);


