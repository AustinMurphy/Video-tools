#!/usr/bin/perl
#
#  Written by Austin Murphy <austin.murphy@gmail.com>, 2011 - 2012
#
#  Search present working directory for videos,  create HTML block on individual page for each
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
#  For each unique videoname, create a page.
#    For each unique dimensions, create an HTML code block
#      For each present format, add that file to the code block
#      Add code for a flashplayer fallback option for older browsers
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
# print out the code blocks
#

foreach my $vid ( sort keys %video_info ) {
  foreach my $dim ( sort keys %{ $video_info{$vid}  } )  {
    my $x, my $y;
    ($x, $y) = split(/x/, $dim);

    my $htmlfile = "$vid.${x}x$y.html";
    #print "filename:  $htmlfile \n\n";
    open(VIDHTML, ">", "$htmlfile");


    #
    # print HTML header text
    #
    
    print VIDHTML "<html>\n";
    print VIDHTML "<head>\n";
    print VIDHTML "<title> Video - $vid.${x}x$y </title>\n";
    print VIDHTML "</head>\n";
    print VIDHTML "\n";
    print VIDHTML "<body>\n";
    print VIDHTML "\n";
    #print "<ul>\n";
    #print "\n";
    #print "\n";


    # not really useful for single-page-per-video style
    #print " <li> $vid @ $x x $y : \n<br>\n";
   
    # jwplayer height incl. controls
    my $w = $y + 24;

    my $mp4url  = "$baseurl/$urldir/$vid.$dim.mp4";
    my $ogvurl  = "$baseurl/$urldir/$vid.$dim.ogv";
    my $webmurl = "$baseurl/$urldir/$vid.$dim.webm";

    # the poster image
    my $posturl = "$baseurl/$urldir/$vid.$dim.preview.jpg";

    print VIDHTML "\n";
    print VIDHTML "<!-- START OF THE PLAYER EMBEDDING TO COPY-PASTE -->\n";
    print VIDHTML "\n";
    print VIDHTML "<video width=\"$x\" height=\"$y\" controls=\"controls\" poster=\"$vid.$dim.preview.jpg\">  \n";

    print VIDHTML "<source src=\"$mp4url\" type=\"video/mp4\"> \n";
    print VIDHTML "<source src=\"$webmurl\" type=\"video/webm\"> \n";
    print VIDHTML "<source src=\"$ogvurl\" type=\"video/ogg\"> \n";

    print VIDHTML "</source> \n";
    print VIDHTML "    <object id=\"player\" classid=\"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000\" name=\"player\" width=\"$x\" height=\"$w\"> \n";
    print VIDHTML "        <param name=\"movie\" value=\"$jwpurl\" /> \n";
    print VIDHTML "        <param name=\"allowfullscreen\" value=\"true\" /> \n";
    print VIDHTML "        <param name=\"allowscriptaccess\" value=\"always\" /> \n";
    print VIDHTML "        <param name=\"flashvars\" value=\"file=$mp4url&image=$posturl\" /> \n";
    print VIDHTML "        <embed \n";
    print VIDHTML "            type=\"application/x-shockwave-flash\" \n";
    print VIDHTML "            id=\"player2\" \n";
    print VIDHTML "            name=\"player2\" \n";
    print VIDHTML "            src=\"$jwpurl\"  \n";
    print VIDHTML "            width=\"$x\"  \n";
    print VIDHTML "            height=\"$w\" \n";
    print VIDHTML "            allowscriptaccess=\"always\"  \n";
    print VIDHTML "            allowfullscreen=\"true\" \n";
    print VIDHTML "            flashvars=\"file=$mp4url&image=$posturl\"  \n";
    print VIDHTML "        /> \n";
    print VIDHTML "    </object> \n";
    print VIDHTML "\n";
    print VIDHTML "</video> \n";
    print VIDHTML "\n";
    print VIDHTML "<!-- END OF THE PLAYER EMBEDDING -->\n";
    print VIDHTML "\n";

    #
    # print HTML footer text
    #
    
    #print "</ul>  \n";
    print VIDHTML "</body>\n";
    print VIDHTML "</html>\n";
    print VIDHTML "\n";
    print VIDHTML "\n";


    close(VIDHTML);

  }
  #print "\n\n\n";
}
#print "\n";





exit;


############################
#
# END
#
############################
