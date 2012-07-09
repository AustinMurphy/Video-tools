#!/usr/bin/perl

use strict;

if ( scalar @ARGV ne '1' ) {
  die "\n  usage:  $0 source_video \n\n";
}

# first arg should be the file to convert
my $video_raw = $ARGV[0];

print "----------------------------------------------------------\n";
print "Source video\n" .
      "------------\n" .
      "  $video_raw \n" .
      "  --\n";


############################
#
#  Constants
#
############################

# helper apps
use constant FFPROBE => "/usr/bin/ffprobe";
use constant FFMPEG => "/usr/bin/ffmpeg";
#use constant WAVEGAIN => "/usr/local/bin/wavegain";
use constant NORMALIZE => "/usr/bin/normalize";
use constant MENCODER => "/usr/bin/mencoder";


# source video contraints
use constant MAX_DURATION => 7500;
use constant MAX_VID_WIDTH => 1920;
use constant MAX_VID_HEIGHT => 1200;
use constant MAX_VID_ASPECT => 2.5;
use constant MIN_VID_ASPECT => 1;

# DAR lookup table
my %dars = (
  "1.33"  =>  "4:3",
  #"1.5"   =>  "3:2",
  "1.50"  =>  "3:2",
  "1.78"  => "16:9",
);

my $realmedia = 0;

############################
#
#  Probe the video file
#
############################

# 
# scrape the container info
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
## dump the data structure
# 
#foreach my $key ( sort keys %fmt_info ) {
#  print " $key  =  $fmt_info{$key} \n";
#}
#print "\n";



#
#    scrape the stream info into variables
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
## 
## dump the data structure
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
# container
# 

# duration
if ( $fmt_info{'duration'} > MAX_DURATION ) {
  die "Source video is too long:  $fmt_info{'duration'} sec, MAX: " . MAX_DURATION . "\n";
}
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
  "$c_filesize bytes \n" ;


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

foreach my $i ( 0 .. $#streams ) {
  if ( $streams[$i]{'codec_name'} eq "rv40" ) {
  print "realmedia audio format found (rv40) \n";
  print "Attempting to convert\n";
  $realmedia = 1;
  }
} 

foreach my $i ( 0 .. $#streams ) {
  if ( $streams[$i]{'codec_name'} eq "rv10" ) {
  print "realmedia audio format found (rv10) \n";
  print "Attempting to convert\n";
  $realmedia = 2;
  }
} 

if ( $j eq -1 ) {
  die "No video stream found\n";
}

# check for multiple stream realmedia files
if ( $j > 1 &&  $fmt_info{'format_name'} eq "rm" ) {
    print "Multiple stream realmedia file found \n" ;
    print "Attempting to convert \n" ;
    $realmedia = 1;
}
my %v_strm =  %{$streams[$j]} ;

# aspect ratio
#
# check for 'display_aspect_ratio' first
#
my $v_aspect='0';
if ( $v_strm{'display_aspect_ratio'} && $v_strm{'display_aspect_ratio'} != 'N/A' ) {
  (my $w, my $h) = split(':', $v_strm{'display_aspect_ratio'} );
  $v_aspect = snap($w, $h);
} else {
  $v_aspect = snap($v_strm{'width'}, $v_strm{'height'} );
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

if ($realmedia == 1) {
 mencoderRm();
}
if ($realmedia == 2) {
 ffmpegRm();
}




############################
#
#  Output specs
#
############################


#
#  
#

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


my $WAV_OUTPUT_FILE = $OUTPUT_FILE . ".wav";
my $MASTER_OUTPUT_FILE = $OUTPUT_FILE . ".master";


print "The following file will be created: \n";
print "  - $WAV_OUTPUT_FILE \n";
print "  - $MASTER_OUTPUT_FILE \n";
print "\n... in the directory : \n";
print " $OUTDIR \n";




# temp
#exit;



############################
#
# CONVERSIONS
#
############################



# 
# WAV extraction
#

# fmpeg -i videoname.source -acodec pcm_s16le -f wav  videoname.wav

my $wav_extr_cmd =  FFMPEG . " -i $video_raw -acodec pcm_s16le -ar 48000 -ac 1 -f wav $WAV_OUTPUT_FILE ";


print "\n\n";
print "Extracting audio track - \n";
print "    Running WAV extraction command: \n $wav_extr_cmd \n";

my $wav_extr_errors = `$wav_extr_cmd 2>/dev/null`;



# 
# WAV dynamic range compression
#

# ffmpeg -drc_scale ...

# Snap to aspect ratio
sub snap {
  (my $width, my $height) = @_;
my $size = 0;
my $ratio;
  if ( $width == 0 ||  $height == 0){
    # divide by zero detected. Prepare for universe collapse.
  }else {
      $ratio = $width/$height ;
      while ( my ($key, $value) = each(%dars) ) {
        if  (abs($key - $ratio) < 0.1) {
        $size = $key; 
        }
     } 
   }
   if (!$size){
     $size = $ratio;
  }
return $size;
}


# 
# WAV normalization
#

# wavegain -y videoname.wav

#my $wav_norm_cmd = WAVEGAIN . " -y $WAV_OUTPUT_FILE ";
my $wav_norm_cmd = NORMALIZE . "  -a -8dBFS  $WAV_OUTPUT_FILE ";

print "\n\n";
print "Normalizing audio track -\n";
print "    Running WAV normalization command: \n $wav_norm_cmd \n";

my $wav_norm_errors = `$wav_norm_cmd 2>/dev/null`;



# 
# MASTER creation
#

# ffmpeg -i videoname.source -vcodec copy -i videoname.wav -acodec copy -f matroska  videoname.master

#my $master_cmd = FFMPEG . " -i $video_raw -vcodec copy -i $WAV_OUTPUT_FILE -acodec copy -f matroska $MASTER_OUTPUT_FILE ";
#my $aspect = scale(
# New FFMPEG syntax (0.10)
my $master_cmd = FFMPEG . " -i $video_raw -i $WAV_OUTPUT_FILE  -map 0:v:0 -c:v copy  -map 1:a:0 -c:a copy -f matroska $MASTER_OUTPUT_FILE ";
#my $master_cmd = FFMPEG . " -i $video_raw -i $WAV_OUTPUT_FILE  -f matroska $MASTER_OUTPUT_FILE ";


print "\n\n";
print "Creating master file from original video track and normalized audio track -\n";
print "    Running master creation command: \n $master_cmd \n";

my $master_errors = `$master_cmd 2>/dev/null`;



#
#
#

print "\n";
#print "\n";


# mencoder -- used to convert realmedia files.
# its a shame that ffmpeg cant do this and surprising since
# mplayer calls on ffmpeg to provide the codecs. 
sub mencoderRm {
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

my $v_aspect='0';
   $v_aspect = snap($v_strm{'width'}, $v_strm{'height'} );

my $CONVERTED_OUTPUT_FILE= $OUTPUT_FILE . ".tmp";

my $rm_convert_cmd =  MENCODER . " $video_raw  -oac lavc -ovc  lavc  aspect=$v_aspect -o $CONVERTED_OUTPUT_FILE ";  

my $converted_errors = `$rm_convert_cmd 2>/dev/null`;

print "Converting file into a format ffmpeg understands. \n" ;
print "Running realmedia conversion command: \n $rm_convert_cmd \n" ;
print "Rerunning conversion scripts. \n" ;

system("convert_video_to_master.pl", "$CONVERTED_OUTPUT_FILE") ;
system("rm $CONVERTED_OUTPUT_FILE");
print " END OF VIDEO CONVERSION SCRIPT \n";
exit;
}


# ffmpeg -- used to convert realmedia files.
# its a shame that ffmpeg cant do this and surprising since
# mplayer calls on ffmpeg to provide the codecs. 
sub ffmpegRm{
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

my $v_aspect='0';
   $v_aspect = snap($v_strm{'width'}, $v_strm{'height'} );

my $CONVERTED_OUTPUT_FILE= $OUTPUT_FILE . ".tmp";

my $rm_convert_cmd = FFMPEG . " -i $video_raw -c:v libx264  -c:a pcm_s16le  -s $v_aspect -f matroska $CONVERTED_OUTPUT_FILE";

my $converted_errors = `$rm_convert_cmd 2>/dev/null`;

print "Converting file into a format ffmpeg understands. \n" ;
print "Running realmedia conversion command: \n $rm_convert_cmd \n" ;
print "Rerunning converion scripts. \n" ;

system("convert_video_to_master.pl", "$CONVERTED_OUTPUT_FILE") ;
#system("rm $CONVERTED_OUTPUT_FILE");
exit;
}


print " END OF VIDEO CONVERSION SCRIPT \n";



exit;


############################
#
# END
#
############################
