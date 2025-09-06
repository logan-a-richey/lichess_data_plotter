#!/usr/bin/perl 

# chess file parser

use strict;
use warnings; 

# get filename from cmdline
my $filename = $ARGV[0];
open(my $fh, '<', $filename) or die "Could not open file. $!\n";

# store the data for a single game
my $record = {};

# read file line by line
print "reading ...\n";
while (my $line = <$fh>) {
    # strip leading and trailing whitespace 
    chomp $line;
    $line =~ s/^\s+|\s+$//g;
    
    # skip empty lines
    next unless $line;
    
    # skip comment lines
    next if ($line =~ /^#/);
    
    # print("$line\n");

    # metadata
    if ($line =~ /^\[/) {
        my ($k, $v) = $line =~ /^\s*\[(\w+)\s*\"(.*?)\".*$/;
       
        # new game - clear record
        if ($k eq "Event") {
            $record = {};
        }

        $record->{$k} = $v;
        next; 
    }

    # pgn data
    if ($line =~ /^1\./) {
        # return a list of clock matches
        (my @clock_values) = $line =~ /\{\s*\[%clk\s*(\d+\:\d+\:\d+)\]\s*\}/g;

        # update the line with clock values and black move \d+... removed
        (my $simple_pgn = $line) =~ s/\{.*?\}//g; 
        $simple_pgn =~ s/\d+\.{3}//g;
        $simple_pgn =~ s/\s+/ /g;

        # store clock values as a stringified list
        my $move_times = "[" . join(', ', @clock_values) . "]";
        
        # debug print
        # print("clock_values => $move_times\n");
        # print("simple_pgn => $simple_pgn\n");
        
        $record->{"move_times"} = $move_times;
        $record->{"pgn"} = $simple_pgn;

    }
}

print "reading - ok\n";




