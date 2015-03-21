use strict;
use warnings;

use Irssi;
my $VERSION = ("0.51");
my %IRSSI = (
	authors => 'djsmiley2k',
	contact => 'djsmiley2k@gmail.com',
	name => 'Old Channel',
	description => 'automatically splits out old channel window; closes older channel window and joins new channel',
	license => 'GPL2',
);

my ($curr_chan, $old_chan);
$curr_chan = Irssi::active_win->{refnum};
$old_chan = Irssi::active_win->{refnum};

sub push_old {
	# Close the old excess window; Push $curr_chan to $old_chan
	if ($old_chan != Irssi::active_win->{refnum}) {
	Irssi::command("/window hide " . $old_chan);
	print "closing old channel";
	$old_chan = $curr_chan;
	print "old chan is $old_chan and curr_chan is $curr_chan";
	} else {
	print "no old channel found";
	$old_chan = $curr_chan;
	$curr_chan = Irssi::active_win->{refnum};
	}
}

sub make_win {
	# Make new window using $old_chan
	# /window show $old_chan
	print "opening old channel in new window";
	Irssi::command("/window show " . $old_chan);
}

Irssi::signal_add_first( 'window changed', \&make_win);
Irssi::signal_add_last( 'window changed', \&push_old);

### Irssi::signal_add_last( 'window changed', \&store_new);


