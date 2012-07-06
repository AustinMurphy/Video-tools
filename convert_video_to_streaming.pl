#!/usr/bin/perl

use strict;
use Getopt::Std;


#
# TODO
#
#  - better bitrate parameters
#  - ?


############################
#
#  Constants
#
############################

# helper apps
use constant FFPROBE => "/usr/bin/ffprobe";
use constant FFMPEG => "/usr/bin/ffmpeg";
use constant QTFS => "/usr/bin/qt-faststart";
use constant FF2T => "/usr/bin/ffmpeg2theora";

# source video contraints
use constant OK_OUT_VID_HEIGHTS => qw( 240 360 480 );
use constant OK_VID_CODECS => qw( avc1 theora vp8 mpeg mpeg2 mpeg4 );
use constant OK_AUD_CODECS => qw( aac vorbis mp3 pcm wav );
use constant MAX_VID_WIDTH => 1920;
use constant MAX_VID_HEIGHT => 1200;
use constant MAX_VID_ASPECT => 2.5;
use constant MIN_VID_ASPECT => 1;

# output parameters
use constant DEF_OUT_VID_HEIGHT => 360;
use constant OUT_AUD_BITRATE => 64;
use constant OUT_AUD_CHAN => 1;
use constant OUT_AUD_SAMPLE_RATE => 48000;

# DAR lookup table
my %dars = (
  "1.33"  =>  "4:3",
  "1.5"   =>  "3:2",
  "1.50"  =>  "3:2",
  "1.78"  => "16:9",
);



############################
#
#     Options
# 
############################

my %opts;
getopt('hir', \%opts); 

#  -i  input file name
my $video_raw ;

#  -r  lines of output resolution (240, 360, 480) 
my $out_vid_height ;


#
# Validate opts
#


#
# filename required
#
exists $opts{h} || !exists $opts{i}   && die "usage:  $0 -i inputfilename [ -r {240|360|480} ] \n";
( $opts{i} ne '' ) || die "ERROR: Input filename required \n";

$video_raw = $opts{i};


#
# make sure given resolution is OK
#
my $out_vid_height_ok = "NOT";
if ( $opts{r} eq '' ) {
  $out_vid_height = DEF_OUT_VID_HEIGHT ;
  $out_vid_height_ok = "OK"; 
}
foreach my $mode ( OK_OUT_VID_HEIGHTS ) {
  if ( $out_vid_height_ok ne "OK" ) {
    #print " testing mode: $mode \n";
    if ( $opts{r} eq $mode ) {
      $out_vid_height = $opts{r};
      $out_vid_height_ok = "OK";
    }
  }
}
( $out_vid_height_ok eq "OK" ) || die "ERROR: unsupported lines of output video resolution: $opts{r} \n";




print "----------------------------------------------------------\n";
print "Source video\n" .
      "------------\n" .
      "  input video:  $video_raw \n" .
      "  --\n" .
      "  output resolution lines:  $out_vid_height \n" .
      "  ------\n" .
      "  input video specs: \n";





############################
#
#  Probe the video file
#
############################

# 
#  scrape the container info
#

open(FORMAT_INFO, FFPROBE . " -show_format $video_raw 2>/dev/null |") or die "Error running ffprobe: $!";

my %fmt_info = ();

while ( <FORMAT_INFO> ) {
  
  chomp;

  if ( /\[FORMAT\]/ ) {

  } elsif ( /\[\/FORMAT\]/ ) {

  } else {
    (my $key, my $val) = split('=');
    #print "key: $key , val: $val \n";
    $fmt_info{$key}=$val;
  }

}
## debug
# 
# dump the data structure
# 
#foreach my $key ( sort keys %fmt_info ) {
#  print " $key  =  $fmt_info{$key} \n";
#}
#print "\n";



#
#  scrape the stream info into variables
#

open(STREAM_INFO, FFPROBE . " -show_streams $video_raw 2>/dev/null |") or die "Error running ffprobe: $!";

my @streams;
my %strm_info;

while ( <STREAM_INFO> ) {
  
  chomp;

  if ( /\[STREAM\]/ ) {

  } elsif ( /\[\/STREAM\]/ ) {
    push @streams, { %strm_info };
    %strm_info = ();

  } else {
    (my $key, my $val) = split('=');
    #print "key: $key , val: $val \n";
    $strm_info{$key}=$val;
  }

}


## debug
# 
# dump the data structure
# 
#foreach my $i ( 0 .. $#streams ) {
#  foreach my $key ( sort keys %{ $streams[$i] } ) {
#    print " $key  =  $streams[$i]{$key} \n";
#  }
#  print "\n";
#}




############################
#
#  Input specs
#
############################


#
# video stream 
#
my $j = -1;
foreach my $i ( 0 .. $#streams ) {
  if ( $streams[$i]{'codec_type'} eq "video" ) {
    $j = $i;
    last;
  }
}
if ( $j eq -1 ) {
  die "No video stream found\n";
}
my %v_strm =  %{$streams[$j]} ;

# aspect ratio
#
# check for 'display_aspect_ratio' first
#
my $v_aspect='0';
if ( $v_strm{'display_aspect_ratio'} && $v_strm{'display_aspect_ratio'} != 'N/A' ) {
  (my $w, my $h) = split(':', $v_strm{'display_aspect_ratio'} );
  $v_aspect = sprintf( "%0.2f", $w/$h );
} else {
  $v_aspect = sprintf( "%0.2f", $v_strm{'width'} / $v_strm{'height'} );
}
if ( $v_aspect < MIN_VID_ASPECT ) {
  die "Source Video Aspect Ratio is too small \n";
}
if ( $v_aspect > MAX_VID_ASPECT ) {
  die "Source Video Aspect Ratio is too large \n";
}
my $dar = $dars{$v_aspect};

# duration
#
my $v_dur_raw =  sprintf( "%0.2f", $v_strm{'duration'} );
my $v_dur_hr =  sprintf( "%02d", $v_dur_raw/3600 );
my $v_dur_min =  sprintf( "%02d", ($v_dur_raw-($v_dur_hr*3600))/60 );
my $v_dur_sec =  sprintf( "%02d", ($v_dur_raw-($v_dur_hr*3600))%60 );

# frame rate
#
# check for 'r_frame_rate' first
#
my $v_frame_rate = "unknown";
if ( $v_strm{'r_frame_rate'} ) {
  (my $n, my $d) = split('/', $v_strm{'r_frame_rate'} );
  $v_frame_rate = sprintf( "%0.2f", $n/$d );
} else {
  $v_frame_rate = sprintf( "%0.2f", $v_strm{'nb_frames'} / $v_strm{'duration'} ); 
};

# video stream summary
print "  V: " . 
  "$v_strm{'codec_name'}, " . 
  "$v_dur_raw sec ($v_dur_hr:$v_dur_min:$v_dur_sec), " . 
  "$v_frame_rate frames/sec, " . 
  $v_strm{'width'}. "x" . $v_strm{'height'} . ", " .
  "DAR: $dar ($v_aspect), " . 
  "$v_strm{'pix_fmt'} \n";


#
#  audio stream
#
my $k = -1;
foreach my $i ( 0 .. $#streams ) {
  if ( $streams[$i]{'codec_type'} eq "audio" ) {
    $k = $i;
    last;
  }
}
if ( $k eq -1 ) {
  die "No audio stream found\n";
}
my %a_strm =  %{$streams[$k]} ;

# duration
#
my $a_dur_raw =  sprintf( "%0.2f", $a_strm{'duration'} );
my $a_dur_hr  =  sprintf( "%02d",  $a_dur_raw/3600 );
my $a_dur_min =  sprintf( "%02d", ($a_dur_raw-($a_dur_hr*3600))/60 );
my $a_dur_sec =  sprintf( "%02d", ($a_dur_raw-($a_dur_hr*3600))%60 );

# sample rate
#
my $a_sample_rate = sprintf( "%d", $a_strm{'sample_rate'} );

# bits_per_sample
#
my $a_bits_sample =  sprintf( "%d", $a_strm{'bits_per_sample'} );
if ($a_bits_sample eq 0) {
  $a_bits_sample = "var.";
}

# audio stream summary
print "  A: " . 
  "$a_strm{'codec_name'}, " .
  "$a_dur_raw sec ($a_dur_hr:$a_dur_min:$a_dur_sec), " . 
  "$a_sample_rate samples/sec, " .
  "$a_bits_sample bits/sample \n" ;


#
# container format
#

# duration
#
my $c_dur_raw =  sprintf( "%0.2f", $fmt_info{'duration'} );
my $c_dur_hr  =  sprintf( "%02d",  $c_dur_raw/3600 );
my $c_dur_min =  sprintf( "%02d", ($c_dur_raw-($c_dur_hr*3600))/60 );
my $c_dur_sec =  sprintf( "%02d", ($c_dur_raw-($c_dur_hr*3600))%60 );

# bitrate
my $c_bitrate = sprintf( "%d", $fmt_info{'bit_rate'} );
# bit_rate

# filesize
my $c_filesize = sprintf( "%d", $fmt_info{'size'} );
# size

# container format summary
print "  C: " . 
  "$fmt_info{'format_name'}, " .
  "$c_dur_raw sec ($c_dur_hr:$c_dur_min:$c_dur_sec), " . 
  "$c_bitrate bits/sec, " .
  "$c_filesize bytes \n" .



############################
#
#  Output specs
#
############################

my $out_v_height ;
my $out_v_width ;

if ( $v_strm{'height'} < $out_vid_height ) {
  $out_v_height =  $v_strm{'height'};
  $out_v_width =  $v_strm{'width'};
  
} else { 
  $out_v_height = $out_vid_height;

  if ( $dars{$v_aspect} ) {
    (my $n, my $d) = split(':', $dars{$v_aspect} );
    my $m = sprintf( "%d", $out_v_height/$d );
    $out_v_width = $m * $n;
  } else {
    $out_v_width = sprintf("%d", $out_v_height * $v_aspect );
  }

}

my $aud_hz;
if ( $a_strm{'sample_rate'} < OUT_AUD_SAMPLE_RATE ) {
  $aud_hz = sprintf( "%d", $a_strm{'sample_rate'} );
} else {
  $aud_hz = OUT_AUD_SAMPLE_RATE;
}


print "\n";
print "\n";


# 
# local directory
#
my $OUTDIR = `pwd`;
chomp $OUTDIR;


#
# output file name 
# 
my $OUTPUT_FILE = $video_raw;
# trim the directories from the front
$OUTPUT_FILE =~ s/^.*\///;
# trim the suffix
$OUTPUT_FILE =~ s/\.[^\.]*$//;
# dots are only for me
$OUTPUT_FILE =~ s/\./_/g;



# 
# shared specs of output formats
#
my $VID_SIZE = $out_v_width . "x" . $out_v_height;
my $VID_FR = "12";

my $MP4_OUTPUT_FILE = $OUTPUT_FILE . "." . $VID_SIZE . ".mp4";
my $OGG_OUTPUT_FILE = $OUTPUT_FILE . "." . $VID_SIZE . ".ogv";
my $WEBM_OUTPUT_FILE = $OUTPUT_FILE . "." . $VID_SIZE . ".webm";



print "The following files will be created: \n";
print "  - $MP4_OUTPUT_FILE \n";
print "  - $OGG_OUTPUT_FILE \n";
print "  - $WEBM_OUTPUT_FILE \n";
print "\n... in the directory : \n";
print " $OUTDIR \n";

print "\n... with the following specs: \n";
print " Video: $VID_SIZE @ $VID_FR fps \n";
print " Audio: " . OUT_AUD_CHAN . " channel(s) @ $aud_hz samples/sec \n";



# temp
#exit;



############################
#
# CONVERSIONS
#
############################


#
# set the specs of the conversions
#

#MP4
my $MP4_FF_VID = "-vcodec libx264 -preset slow -profile:v  baseline -crf 23 -keyint_min 0 -g 250 -skip_threshold 0 -qmin 10 -qmax 51" ;
my $MP4_FF_AUD = "-acodec libfaac -ab " . OUT_AUD_BITRATE ."k -ac " . OUT_AUD_CHAN . " -ar $aud_hz -async 400";

#OGG
my $FF2T_VID = "-v 6 --speedlevel 0";
my $FF2T_AUD = "-A " . OUT_AUD_BITRATE . " -c " . OUT_AUD_CHAN . " -H $aud_hz";

#WEBM
my $WEBM_FF_VID = "-vcodec libvpx -keyint_min 0 -g 250 -skip_threshold 0 -qmin 10 -qmax 51 -crf 23";
my $WEBM_FF_AUD = "-acodec libvorbis -ab " . OUT_AUD_BITRATE ."k -ac " . OUT_AUD_CHAN . " -ar $aud_hz -async 400";



# 
# MP4 conversion
#

my $mp4_cmd = FFMPEG . " -threads 12 -i $video_raw $MP4_FF_VID -s $VID_SIZE -r $VID_FR $MP4_FF_AUD -f mp4 $MP4_OUTPUT_FILE-tmp ";

# need to convert tmp to real (qt-faststart)
my $mp4_cmd_qt = QTFS . " $MP4_OUTPUT_FILE-tmp $MP4_OUTPUT_FILE ";

print "\n\n";
print "Streaming format 1 - h264/aac/mp4 \n";

print "\n";
print "Running MP4 conversion command: \n $mp4_cmd \n";

my $mp4_errors = `$mp4_cmd 2>/dev/null`;

print "\n";
print "Running MP4 qtfs command: \n $mp4_cmd_qt \n";

my $mp4qt_errors = `$mp4_cmd_qt 2>/dev/null`;
my $mp4qt_rm_errors = `rm -f $MP4_OUTPUT_FILE-tmp 2>/dev/null`;



# 
# OGG conversion
#

my $ogg_cmd = FF2T . " $FF2T_VID -x $out_v_width -y $out_v_height -F $VID_FR $FF2T_AUD -o $OGG_OUTPUT_FILE $video_raw ";

print "\n\n";
print "Streaming format 2 - theora/vorbis/ogg \n";

print "\n";
print "Running OGG conversion command: \n $ogg_cmd \n";

my $ogg_errors = `$ogg_cmd 2>/dev/null`;



# 
# WEBM conversion
#

my $webm_cmd = FFMPEG . " -threads 12 -i $video_raw $WEBM_FF_VID -s $VID_SIZE -r $VID_FR $WEBM_FF_AUD -f webm $WEBM_OUTPUT_FILE ";

print "\n\n";
print "Streaming format 3 - vp8/vorbis/webm \n";

print "\n";
print " Running WEBM conversion command: \n $webm_cmd \n";

my $webm_errors = `$webm_cmd 2>/dev/null`;



print "\n";
#print "\n";

print " END OF VIDEO CONVERSION SCRIPT \n";

exit;


############################
#
# END
#
############################
