use strict;
use warnings;

use Irssi;
my $VERSION = ("0.5");
my %IRSSI = (
	authors => 'djsmiley2k',
	contact => 'djsmiley2k@gmail.com',
	name => 'Old Channel',
	description => 'automatically splits out old channel window; closes older channel window and joins new channel',
	license => 'GPL2',
);

my ($curr_chan, $old_chan);
store_new

sub push_old {
	# Push $curr_chan to $old_chan
	if (defined $old_chan) {
	Irssi::command("/window hide " . $old_chan);
	}
	$old_chan = $curr_chan;
}

sub make_win {
	# Make new window using $old_chan
	# /window show $old_chan
	Irssi::command("/window show " . $old_chan);
}

sub store_new {
	# store new channel name in $curr_chan
	$curr_chan = Irssi::active_win->{refnum};
	
}

Irssi::signal_add_first( 'window changed', \&push_old);
Irssi::signal_add_last( 'window changed', \&make_win);
Irssi::signal_add_last( 'window changed', \&store_new);


