#!/usr/bin/perl

use strict;

use constant convert_to_master => "/usr/local/bin/convert_video_to_master.pl";
use constant convert_to_stream => "/usr/local/bin/convert_video_to_streaming.pl";


foreach my $argnum (0 .. $#ARGV) {

my $filename =  $ARGV[$argnum];

print "$filename \n" ;


if (-e $filename) {
 print "File Exists! \n";

print" converting to master. \n";

my $convertm_cmd = convert_to_master . " $ARGV[$argnum]";
print " $convertm_cmd \n";

system($convertm_cmd);


my $OUTPUT_FILE = $filename;
# trim the directories from the front
$OUTPUT_FILE =~ s/^.*\///;
# trim the suffix
$OUTPUT_FILE =~ s/\.[^\.]*$//;
# dots are only for me
$OUTPUT_FILE =~ s/\./_/g;

print "converting to stream. \n";
sleep 1;
my $MASTER_INPUT_FILE = $OUTPUT_FILE . ".master";
#my $MASTER_OUTPUT_FILE = $OUTPUT_FILE . ".master";


#if (-e $MASTER_INPUT_FILE) {
# print "File Exists!";

my $converts_cmd = convert_to_stream . " -i  $MASTER_INPUT_FILE";

print " $converts_cmd \n";

system($converts_cmd);

}
}


exit;
