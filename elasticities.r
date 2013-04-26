setwd("/Users/joannahsu/Documents/Courses/datamining290/code")
data=read.csv("price-elasticity.csv")

clean <- function(ttt){as.numeric( gsub('[^a-zA-Z0-9.]', '', ttt))} #drops all dollar signs , etc
data[] <- sapply(data, clean) 

#regressions
weekends=subset(data, DOW>=6)
plot(weekends$Rooms, weekends$Rate)
plot(log(weekends$Rooms), log(weekends$Rate))
mWE=lm(log(weekends$Rooms)~log(weekends$Rate))
mWE2=lm(log(weekends$Rate)~log(weekends$Rooms))
summary(mWE)

weekdays=subset(data, DOW<6)
plot(weekdays$Rooms, weekdays$Rate)
plot(log(weekdays$Rooms), log(weekdays$Rate))
mWD=lm(log(weekdays$Rooms)~log(weekdays$Rate))
mWD2=lm(log(weekdays$Rate)~log(weekdays$Rooms))
summary(mWD)


#Price elasticity of weekdays: -1.7630 #coef(mWD)[2]
#Price elasticity of weekends: -1.4369 #coef(mWE)[2]

results=matrix(NA, 5000, 4)
for (iPrice in 1:5000)
{
Q=as.numeric(round(exp(coef(mWE)[1]+coef(mWE)[2]*log(iPrice))),0)
TotalRevenue=iPrice*Q
possible=ifelse (Q<=100, TRUE, FALSE)  #only have 100 rooms to sell
results[iPrice, ]=c(iPrice, Q, TotalRevenue, possible)
}
results=as.data.frame(results)
names(results)=c("Price", "RoomsSold", "TotalRevenue", "possible")
resultsWE=subset(results, possible==TRUE)

#repeat for weekdays
results=matrix(NA, 5000, 4)
for (iPrice in 1:5000)
{
Q=as.numeric(round(exp(coef(mWD)[1]+coef(mWD)[2]*log(iPrice))),0)
TotalRevenue=iPrice*Q
possible=ifelse (Q<=100, TRUE, FALSE)
results[iPrice, ]=c(iPrice, Q, TotalRevenue, possible)
}
results=as.data.frame(results)
names(results)=c("Price", "RoomsSold", "TotalRevenue", "possible")
resultsWD=subset(results, possible==TRUE)



par(mfrow=c(2,3), mar=c(12,6,1,3), oma=c(2,2,2,2),cex.main=1)
plot(log(weekdays$Rate), log(weekdays$Rooms), xlab="log(Rate)", ylab="log(Rooms)",main="weekdays")
plot(resultsWD$Price, resultsWD$TotalRevenue, xlab="Room Rate", ylab= "total revenue",main="weekdays") #craziness is from rounding
plot(resultsWD$RoomsSold, resultsWD$TotalRevenue, xlim=c(0,100), ylab= "total revenue",xlab="Rooms Sold", main=" weekdays")
plot(log(weekends$Rate), log(weekends$Rooms), xlab="log(Rate)", ylab="log(Rooms)",main="weekends")
plot(resultsWE$Price, resultsWE$TotalRevenue, xlab="Room Rate", ylab= "total revenue",main=" weekends")
plot(resultsWE$RoomsSold, resultsWE$TotalRevenue, xlim=c(0,100), ylab= "total revenue",xlab="Rooms Sold", main="weekends")

#is this reasonable?
data.s=data[order(data$Rate),]
