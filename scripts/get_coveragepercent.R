library(dplyr)
CAMI_counts <- read.csv("~/CAMI_counts.csv", row.names=1)
colnames(CAMI_counts) = c("sample0", "sample1", "sample2", "sample3", "sample4", "sample5", "sample6", "sample7", "sample8", "sample9")

for (x in colnames(CAMI_counts)) {
  df = CAMI_counts[x]
  colnames(df) = c("sample")
  df = df %>%
    mutate(freq = (sample / sum(sample, na.rm = T))*100)
  df=df["freq"]
  colnames(df) = x
  df = na.omit(df)
  write.csv(df, file=paste(x, "_cov.csv", sep = ''))
}
