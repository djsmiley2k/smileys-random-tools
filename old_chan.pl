


use Irssi;
%VERSION = '0.1';
%IRSSI = (
	authors => 'djsmiley2k',
	contact => 'djsmiley2k@gmail.com',
	name => 'Old Channel',
	description => 'automatically splits out old channel window; closes older channel window and joins new channel',
	license => 'GPL2',
);

# Let's put the variables outside the scope of the subs, so that they behave a little more like globals.
my ($old_chan,$curr_chan,$new_win);

sub push_old {
	# Push $curr_chan to $old_chan
	$old_chan = $curr_chan
}

sub make_win {
	# Make new window using $old_chan
	# /window show $old_chan
	$new_win = Irssi::command("/WINDOW split" $old_chan"");
}

sub store_new {
	# store new channel name in $curr_chan
	$curr_chan = Irssi::active_win()
}


