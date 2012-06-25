#!/usr/bin/perl
#
#  Written by Austin Murphy <austin.murphy@gmail.com>, 2011
#
#  Search present working directory for videos,  create HTML block for each in a common page
#
#
#   Assumes files are named like this:
#
#         videoname.dimensions.format 
#
#  Where format := {mp4, ogv, webm} 
#  and there could be multiple values for dimensions
#
#
#  For each unique dimensions, create an HTML code block
#    For each present format, add that file to the code block
#    Add code for a flashplayer fallback option for older browsers
#  

#
#  STATUS:  This script works, but is kind of dumb about some things
#

#  ******** NOTE ********
#
#  Set $baseurl to something useful for you...
#
#  ******** NOTE ********



use strict;

if ( scalar @ARGV ne '0' ) {
  die "\n  usage:  $0 \n\n";
}



#
#  Constants
#

#
my $baseurl = "http://video.server.example.com";

# valid formats
use constant FORMATS => qw( mp4 ogv webm );

# jwplayer location
my $jwpurl = "$baseurl/pub/flash/jwplayer/player.swf";


#
# user & location info
#

my $user = `whoami`;
chomp $user;

my $dir = `pwd`;
chomp $dir;

my $urlsubdirs;

my @parts = split(/\//, $dir);
#print "0: $parts[0], 1: $parts[1], 2: $parts[2], 3: $parts[3], 4: $parts[4], 5: $parts[5] \n";
if ( $parts[1] == "home" ) {
  shift @parts;
  shift @parts;
  shift @parts;
  shift @parts;
  shift @parts;
  $urlsubdirs = join('/', @parts );
} elsif ( $parts[1] == "data" ) {
  shift @parts;
  shift @parts;
  shift @parts;
  shift @parts;
  shift @parts;
  $urlsubdirs = join('/', @parts );
} else {
  die "bad directory \n";
}

my $urldir = "$user/$urlsubdirs";


# 
# scrape the directory info
#

open(VIDEO_LIST, "ls -1 |") or die "Error running ls: $!";

my %video_info;

while ( <VIDEO_LIST> ) {
  
  chomp;
  foreach my $fmt ( FORMATS ) {
    if (/$fmt/) {
      split(/\./) ;
      $video_info{$_[0]}{$_[1]}{$_[2]} = 1;
    }
  }

}
## debug
# 
# dump the data structure
# 
#foreach my $vid ( sort keys %video_info ) {
#  print "$vid \n";
#  foreach my $dim ( sort keys %{ $video_info{$vid}  } )  {
#    print "  $dim \n";
#    foreach my $fmt ( sort keys %{ $video_info{$vid}{$dim} } ) {
#      print "    $fmt \n";
#    }
#  }
#  print "\n";
#}
#print "\n";



#
# print HTML header text
#

print "<html>\n";
print "<head>\n";
print "<title> sample video </title>\n";
print "</head>\n";
print "\n";
print "<body>\n";
print "\n";
print "<ul>\n";
print "\n";
print "\n";



#
# print out the code blocks
#

foreach my $vid ( sort keys %video_info ) {
  foreach my $dim ( sort keys %{ $video_info{$vid}  } )  {
    my $x, my $y;
    ($x, $y) = split(/x/, $dim);
    print " <li> $vid @ $x x $y : \n<br>\n";
   
    # jwplayer height incl. controls
    my $w = $y + 24;

    my $mp4url  = "$baseurl/$urldir/$vid.$dim.mp4";
    my $ogvurl  = "$baseurl/$urldir/$vid.$dim.ogv";
    my $webmurl = "$baseurl/$urldir/$vid.$dim.webm";

    # the poster image
    my $posturl = "$baseurl/$urldir/$vid.$dim.preview.jpg";

    print "\n";
    print "<!-- START OF THE PLAYER EMBEDDING TO COPY-PASTE -->\n";
    print "\n";
    print "<video width=\"$x\" height=\"$y\" controls=\"controls\" poster=\"$vid.$dim.preview.jpg\">  \n";

    print "<source src=\"$mp4url\" type=\"video/mp4\"> \n";
    print "<source src=\"$webmurl\" type=\"video/webm\"> \n";
    print "<source src=\"$ogvurl\" type=\"video/ogg\"> \n";

    print "</source> \n";
    print "    <object id=\"player\" classid=\"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000\" name=\"player\" width=\"$x\" height=\"$w\"> \n";
    print "        <param name=\"movie\" value=\"$jwpurl\" /> \n";
    print "        <param name=\"allowfullscreen\" value=\"true\" /> \n";
    print "        <param name=\"allowscriptaccess\" value=\"always\" /> \n";
    print "        <param name=\"flashvars\" value=\"file=$mp4url&image=$posturl\" /> \n";
    print "        <embed \n";
    print "            type=\"application/x-shockwave-flash\" \n";
    print "            id=\"player2\" \n";
    print "            name=\"player2\" \n";
    print "            src=\"$jwpurl\"  \n";
    print "            width=\"$x\"  \n";
    print "            height=\"$w\" \n";
    print "            allowscriptaccess=\"always\"  \n";
    print "            allowfullscreen=\"true\" \n";
    print "            flashvars=\"file=$mp4url&image=$posturl\"  \n";
    print "        /> \n";
    print "    </object> \n";
    print "\n";
    print "</video> \n";
    print "\n";
    print "<!-- END OF THE PLAYER EMBEDDING -->\n";
    print "\n";
  }
  print "\n\n\n";
}
print "\n";



#
# print HTML footer text
#

print "</ul>  \n";
print "</body>\n";
print "</html>\n";
print "\n";
print "\n";



exit;


############################
#
# END
#
############################
