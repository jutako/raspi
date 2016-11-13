
#install.packages('lubridate')
require('lubridate')
require('stats')

inpath <- '/home/jussi/Dropbox/Data/thingspeak/envlogger/'
outpath <- '/home/jussi/Dropbox/Code/github/raspi/thingspeak/envlogger/'
infile <- 'feeds.csv'
K <- 5

d <- read.table(file.path(inpath, infile), sep = ',', stringsAsFactors = F)
str(d)
names(d) <- c('time','id','temp','hum','temp2','hum2')

d$time <- lubridate::ymd_hms(d$time, tz = 'Europe/Helsinki')
d[, c('temp','hum','temp2','hum2')] <- as.numeric(as.matrix(d[, c('temp','hum','temp2','hum2')]))

d$temp <- stats::runmed(d$temp, K, endrule = "constant")
d$hum <- stats::runmed(d$hum, K, endrule = "constant")

na.runmed <- function(dvec, k){
  na.match <- is.na(dvec)
  dvec[!na.match] <- stats::runmed(dvec[!na.match], k, endrule = 'constant')
  dvec
}
d$temp2 <- na.runmed(d$temp2, K)
d$hum2 <- na.runmed(d$hum2, K)
d  <- d[!is.na(d$time),]

dout <- data.frame(Date = format(d$time, format = "%Y/%m/%d %H:%M:%S"),
                   Series1 = d$temp,
                   Series2 = d$temp2)
write.table(dout,
            file = file.path(outpath, 'envlogger_temp.csv'),
            sep = ",",
            row.names = F,
            na = "",
            quote = F)
