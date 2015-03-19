


use Irssi;
%VERSION = '0.2';
%IRSSI = (
	authors => 'djsmiley2k',
	contact => 'djsmiley2k@gmail.com',
	name => 'Old Channel',
	description => 'automatically splits out old channel window; closes older channel window and joins new channel',
	license => 'GPL2',
);
my $curr_chan = Irssi::active_win();


sub push_old {
	# Push $curr_chan to $old_chan
	Irssi::command("/Window hide " $old_chan);
	my $old_chan = $curr_chan;
}

sub make_win {
	# Make new window using $old_chan
	# /window show $old_chan
	Irssi::command("/WINDOW split " $old_chan);
}

sub store_new {
	# store new channel name in $curr_chan
	my $curr_chan = Irssi::active_win();
	
}

Irssi::signal_add_first( 'window item changed', \&push_old);
Irssi::signal_add_last( 'window item changed', \&make_win);
Irssi::signal_add_last( 'window item changed' \&store_new);


