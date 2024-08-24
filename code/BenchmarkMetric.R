## Load the relevant libraries
suppressPackageStartupMessages({
    library(GenomicRanges)
    library(dplyr)
    library(openxlsx)
})

coords_to_bed = function(coords){
    seqs = strsplit(coords, ":")
    chrs = unlist(lapply(seqs, "[[", 1))
    range = unlist(lapply(seqs, "[[", 2))
    range = strsplit(gsub(",","",range), "-")
    start = unlist(lapply(range, "[[", 1))
    end = unlist(lapply(range, "[[", 2))
    return(list(chrs, start, end))
}

## Set working directory where scoring tables are stored (Epi and SSv4)
setwd("./scoring_tables")

#####################################################
## Epifolourscence scoring
#####################################################

## Load in flouresence scoring sheet
epi.table = read.xlsx("BICCN_fluorescence_scoring_sheet.xlsx")

## Rename to a machine readable format
epi.table$liftover = epi.table["Liftover_coordinates.(Alt-Species)"]

## Keep all mouse enhancers and filter out human enhancers without mouse liftover
epi.score.table = epi.table %>% filter(!is.na(liftover) | Species == "Mouse")

## Gather coordinates
coords_species = coords_to_bed(epi.score.table["Coordinates.Enhancer.(Species)"][,1])
coords_alt_species = epi.score.table %>% 
                        filter(Species == "Human") %>% 
                        pull(liftover) %>% 
                        pull(1) %>% 
                        coords_to_bed

## Add in chr, start, end 
epi.score.table = cbind("chr"=coords_species[[1]], 
                        "start"=coords_species[[2]], 
                        "end"=coords_species[[3]],
                        epi.score.table)

## Set chr, start, end to human liftover for human sequences
epi.score.table[which(epi.score.table$Species == "Human"),"chr"] = coords_alt_species[[1]]
epi.score.table[which(epi.score.table$Species == "Human"),"start"] = coords_alt_species[[2]]
epi.score.table[which(epi.score.table$Species == "Human"),"end"] = coords_alt_species[[3]]

## Gather on-target cell populations
epi.score.table$LABELED_CELL_POPULATION = epi.score.table$max_subclass_primary
epi.score.table$LABELED_CELL_POPULATION_ALT = epi.score.table$max_subclass_Secondary

## Build final epifold scoring table
epi.score.table = makeGRangesFromDataFrame(epi.score.table[,c("chr", "start", "end", 
                                        "Enhancer_ID", 
                                        "LABELED_CELL_POPULATION", "LABELED_CELL_POPULATION_ALT",
                                        "LABEL_Specificity", "LABEL_Brightness")], keep.extra.columns=TRUE)

## Create a modulating score based on brightness
epi.score.table$SCORE = 1
epi.score.table$SCORE[which(epi.score.table$LABEL_Brightness== "strong")] = 2
epi.score.table$SCORE[which(epi.score.table$LABEL_Brightness == "weak")] = 1.5

## We didn't distinguish between Lamp5 and Lamp_Lhx6 when asking teams to score, put all to Lamp5
epi.score.table$LABELED_CELL_POPULATION = gsub("Lamp_Lhx6|Lamp5_Lhx6", "Lamp5", epi.score.table$LABELED_CELL_POPULATION)
epi.score.table$LABELED_CELL_POPULATION_ALT = gsub("Lamp_Lhx6|Lamp5_Lhx6", "Lamp5", epi.score.table$LABELED_CELL_POPULATION_ALT)

#####################################################
## SSv4 scoring
#####################################################

## Read in the ssv4 table and filter down to enhancers that exist in epiflourescence scoring
ssv4.table = read.xlsx("BICCN_SSv4_scoring_sheet.xlsx")
ssv4.table = ssv4.table %>% filter(Enhancer_ID %in% epi.score.table$Enhancer_ID)

## Gather coordinates parts
ssv4.table$chr = as.character(seqnames(epi.score.table[match(ssv4.table$Enhancer_ID, epi.score.table$Enhancer_ID),]))
ssv4.table$start = start(epi.score.table[match(ssv4.table$Enhancer_ID, epi.score.table$Enhancer_ID),])
ssv4.table$end = end(epi.score.table[match(ssv4.table$Enhancer_ID, epi.score.table$Enhancer_ID),])

## Gather cell type labels and scores
ssv4.table$LABELED_CELL_POPULATION = epi.score.table[match(ssv4.table$Enhancer_ID, epi.score.table$Enhancer_ID),]$LABELED_CELL_POPULATION
ssv4.table$SCORE = epi.score.table[match(ssv4.table$Enhancer_ID, epi.score.table$Enhancer_ID),]$SCORE

## Update column names
colnames(ssv4.table) = gsub("\\.", "-", colnames(ssv4.table))

## Create final ssv4 scoring table
ssv4.score.table = makeGRangesFromDataFrame(ssv4.table[,c("chr", "start", "end", "Enhancer_ID", colnames(ssv4.table)[4:ncol(ssv4.table)])], keep.extra.columns=TRUE)

#####################################################
## Challenge scoring
#####################################################
## Function to score a team's submission
biccn_scoring = function(bed.file, epi.score.table, ssv4.score.table){

    ## Only keep rows without NAs (edge case for some teams submissions)
    bed.file = bed.file[rowSums(is.na(bed.file)) == 0,]

    ## Rename columns in case of any issue in teams file, assuming ordering otherwise the following will fail.
    colnames(bed.file) = c("chr", "start", "end", "subclass_Bakken_2022", "rank")

    ## Rename to match scoring tables
    team.bed = makeGRangesFromDataFrame(bed.file, keep.extra.columns=TRUE)
    team.bed$subclass_Bakken_2022 = gsub("L2/3 IT", "L2-3_IT", team.bed$subclass_Bakken_2022)
    team.bed$subclass_Bakken_2022 = gsub("L4/5 IT", "L4_IT", team.bed$subclass_Bakken_2022)
    team.bed$subclass_Bakken_2022 = gsub("L5 ET", "L5_ET", team.bed$subclass_Bakken_2022)
    team.bed$subclass_Bakken_2022 = gsub("L5 IT", "L5_IT", team.bed$subclass_Bakken_2022)
    team.bed$subclass_Bakken_2022 = gsub("L5/6 NP", "L5-6_NP", team.bed$subclass_Bakken_2022)
    team.bed$subclass_Bakken_2022 = gsub("L6 CT", "L6_CT", team.bed$subclass_Bakken_2022)
    team.bed$subclass_Bakken_2022 = gsub("L6 IT", "L6_IT", team.bed$subclass_Bakken_2022)
    team.bed$subclass_Bakken_2022 = gsub("L6 IT Car3", "L6_IT_Car3", team.bed$subclass_Bakken_2022)
    team.bed$subclass_Bakken_2022 = gsub("Sst Chodl", "Sst_Chodl", team.bed$subclass_Bakken_2022)
    team.bed$subclass_Bakken_2022 = gsub("Micro-PVM", "Micro_PVM", team.bed$subclass_Bakken_2022)

    ## Stores results aggregated for Epi, SSv4, and leaderboard (Sum of SSv4/Epi)
    team.score = data.frame(celltype=character(), score = numeric())

    ## Stores results per-enhancer
    team.score.full = data.frame(celltype=character(), score=numeric(), enhancer=character())

    ## 
    for(celltype in unique(epi.score.table$LABELED_CELL_POPULATION)){
        ## Gather team results for current celltype.
        team.bed.ct = team.bed[which(team.bed$subclass_Bakken_2022 == celltype),]
        ## Gather scoring data for current celltype.
        ct.score.table = epi.score.table[which(epi.score.table$LABELED_CELL_POPULATION == celltype),]
        ## Give some relaxation to coordinates
        overlap.res = findOverlaps(ct.score.table+1000, team.bed.ct) 
        ## With relaxation we pick up multiple matches to the same enhancer, remove duplicates. 
        ## Duplicates are removed such that only the highest ranking peak in the region is retained. 
        overlap.res = overlap.res[!duplicated(queryHits(overlap.res)),]
        ## Gather scoring data for enhancers that team picked up on
        scoring = ct.score.table[queryHits(overlap.res),] %>% as.data.frame()
        ##
        if(nrow(scoring) > 0){
            ## Setup how teams will be scored based on Enhancer categories. More weight given to On-Target than the other scoring categories.
            scoring$direction = 1
            scoring$direction[which(scoring$LABEL_Specificity %in% c("On-Target"))] = -1
            scoring$direction[which(scoring$LABEL_Specificity %in% c("Mixed-Target"))] = 0.5
            ## Epi Metric:
            ##      Specificity (direction) is weighted by SCORE (Brightness converted to integer) and the 
            ##      rank of the associated enhancer in the team's submission.
            score = scoring$SCORE * scoring$direction * (10000 - as.integer(team.bed.ct[subjectHits(overlap.res),]$rank))
            ## Add per-enhancer results to full scoring table
            team.score.full = rbind(team.score.full, data.frame("team_celltype" = celltype, "score" = score, "enhancer" = scoring$Enhancer_ID))
            ## Handle all missing enhancers by giving the worse score possible (10000) which is good for Off-Target / No-Labeling!
            score = (sum(score) + (10000 * (length(ct.score.table) - nrow(scoring)))) / 10000
            ##
        }else{
            ## If a team missed all enhancers
            score = length(ct.score.table)
        }
        ##
        team.score[nrow(team.score)+1,] = c(celltype, score)
    }

    #####################################################
    ## SSv4
    #####################################################

    ## 
    for(celltype in unique(ssv4.score.table$LABELED_CELL_POPULATION)){
        ## Gather team results for current celltype.
        team.bed.ct = team.bed[which(team.bed$subclass_Bakken_2022 == celltype),]
        ## Gather scoring data for current celltype.
        ct.score.table = ssv4.score.table[which(ssv4.score.table$LABELED_CELL_POPULATION == celltype),]
        ## Give some relaxation to coordinates
        overlap.res = findOverlaps(ct.score.table+1000, team.bed.ct) 
        ## With relaxation we pick up multiple matches to the same enhancer, remove duplicates. 
        ## Duplicates are removed such that only the highest ranking peak in the region is retained. 
        overlap.res = overlap.res[!duplicated(queryHits(overlap.res)),]
        ## Gather scoring data for enhancers that team picked up on
        scoring = ct.score.table[queryHits(overlap.res),] %>% as.data.frame()
        colnames(scoring) = gsub("\\.","-", colnames(scoring))
        ##
        if(nrow(scoring) > 0){
            ## SSv4 Metric:
            ##      Specificity is weighted by SCORE (Brightness converted to integer), the 
            ##      SSv4 quantification for the target cell type (scoring[,celltype]) and
            ##      the rank of the associated enhancer in the team's submission.
            score = scoring$SCORE * (10000 - as.integer(team.bed.ct[subjectHits(overlap.res),]$rank)) / (1 + scoring[,celltype])
            ## Add per-enhancer results to full scoring table
            team.score.full = rbind(team.score.full, data.frame("team_celltype" = paste0(celltype, "_SSv4"), "score" = score, "enhancer" = scoring$Enhancer_ID))
            ## Handle all missing enhancers by giving the worse score possible (10000) which is good for Off-Target / No-Labeling!
            score = (sum(-score) + (10000 * (length(ct.score.table) - nrow(scoring)))) / 10000
        }else{
            score = length(ct.score.table)
        }
        ##score
        team.score[nrow(team.score)+1,] = c(paste0(celltype, "_SSv4"), score)
    }
    team.score$leaderboard_score = sum(as.numeric(team.score$score))
    return(list(team.score, team.score.full))
}

## ----------------------------------------
## EXAMPLE

##
# bed.file = read.csv("/allen/programs/celltypes/workgroups/rnaseqanalysis/EvoGen/BICCN_Challenge/ArchR/results_full_update.csv")

## Run scoring
# scored.bed = biccn_scoring(bed.file, epi.score.table, ssv4.score.table)
