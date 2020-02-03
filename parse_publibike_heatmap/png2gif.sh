# create gif from png

# slows down by 2x
# gif
ffmpeg -pattern_type glob -i 'results/*.png' -filter:v "setpts=2.0*PTS" results/out.gif -y
# mp4
ffmpeg -pattern_type glob -i 'results/*.png' -filter:v "setpts=2.0*PTS" results/out.mp4 -y

#https://gist.github.com/nikhan/26ddd9c4e99bbf209dd7
# for twitter
ffmpeg -pattern_type glob -i 'results/*.png' -vcodec libx264 -vf 'setpts=2.0*PTS,scale=640:trunc(ow/a/2)*2' \
    -acodec aac -vb 1024k -minrate 1024k -maxrate 1024k -bufsize 1024k \
    -pix_fmt yuv420p \
    -ar 44100 -strict experimental -r 30 results/out.mp4

# clean dates to be only full days
rm -f results/publibike_20200125_*.png results/publibike_20200202_*.png
# or 
mv results/publibike_20200202_*.png ignore
mv results/publibike_20200125_*.png ignore 

# could also do this with imagemagick/convert
# convert results/*.png results/out.gif