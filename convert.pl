#!/usr/bin/perl

use File::Basename;
use File::Path qw(mkpath);
use strict;

use constant convert_to_master => "/usr/local/bin/convert_video_to_master.pl";
use constant convert_to_stream =>
  "/usr/local/bin/convert_video_to_streaming.pl";

#Home Directory PATH
my $HOMEDIR = $ENV{"HOME"};

#check for video directory.
my $directory = "$HOMEDIR/videos";
if ( -e $directory ) {

    # needs check
}

my $numArgs = $#ARGV + 1;

#check for input. If none, run from upload directory.
if ( $numArgs == 0 ) {

    #copy folder tree into the master directory.
    my $orig = "$HOMEDIR/videos/upload/";
    my $new  = "$HOMEDIR/videos/masters/";

    print "Copying folder tree into masters directory \n\n";

    copyDirTree( $orig, $new );

    setPath($orig);

    #fild all files in the original directory
    my @files = (`find $HOMEDIR/videos/upload/  -type f`);
    foreach my $file (@files) {

        ( my $fileBaseName, my $dirName, my $fileExtension ) = fileparse($file);

        my $outputFile = $file;
        $outputFile = $dirName;
        $dirName =~ s/upload/masters/;

        setPath($dirName);
        print "setpath to $dirName\n";
        convertToMaster($file);
    }

    $orig = "$HOMEDIR/videos/masters/";
    $new  = "$HOMEDIR/videos/public/";

    copyDirTree( "/home/kbende/videos/masters/",
        "/home/kbende/videos/public/" );

    setPath($new);

    #fild all files in the master directory
    my @files = (`find $HOMEDIR/videos/masters/  -type f`);
    print "@files\n";
    foreach my $file (@files) {

        ( my $fileBaseName, my $dirName, my $fileExtension ) = fileparse($file);
        print "$fileExtension";
        if ( $fileExtension == ".master" ) {
            my $outputFile = $file;
            $outputFile = $dirName;
            $dirName =~ s/masters/public/;

            setPath($dirName);
            print "setpath to $dirName\n";
            convertToStream($file);
        }
    }
}

if ( $numArgs >= 1 ) {
    foreach my $argnum ( 0 .. $#ARGV ) {
        my $filename = $ARGV[$argnum];
        convertToMaster($filename);
    }
}
# convert media file to master
sub convertToMaster() {
    ( my $inputFile ) = @_;
    print "$inputFile\n";
    print "File Exists! \n";
    print " converting to master. \n";
    my $convertm_cmd = convert_to_master . " $inputFile";
    print " $convertm_cmd \n";
    system($convertm_cmd);
}

# convert master file to streaming
sub convertToStream() {
    ( my $MASTER_INPUT_FILE ) = @_;
    print "converting to stream. \n";
    my $converts_cmd = convert_to_stream . " -i  $MASTER_INPUT_FILE";
    print " $converts_cmd \n";
    system($converts_cmd);
}

#copy directory tree
#the newer version of perl includes a package that does this for you. If
# you are wondering why i am doing it this way, dont, it works and Ill make it
# nicer when the newer version gets installed.
sub copyDirTree() {
    ( my $inputDir, my $outputDir ) = @_;
    print "input $inputDir ... output $outputDir\n";
    setPath($inputDir);

    my @dirs = `find * -type d -print`;
    print "dirs =  @dirs\n";
    foreach my $dirs (@dirs) {
        chomp($dirs);
        setPath($outputDir);
        print "$dirs \n";
        mkpath($dirs);
    }
}

#set dir path
sub setPath() {
    ( my $dir ) = @_;
    print "Moving to directory $dir";
    chdir($dir) or die "Cannot chdir to $dir: $!";
}

#strip extenstions from filename
#I stole this code from Austin. :)
sub strip () {
    ( my $filename ) = @_;

    my $OUTPUT_FILE = $filename;

    # trim the directories from the front
    $OUTPUT_FILE =~ s/^.*\///;

    # trim the suffix
    $OUTPUT_FILE =~ s/\.[^\.]*$//;

    # dots are only for me
    $OUTPUT_FILE =~ s/\./_/g;
    return $OUTPUT_FILE;
}

exit;
