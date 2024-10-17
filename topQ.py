from Bio import SeqIO

def calculate_average_quality(qualities):
    """Calculate the average quality score for a list of quality scores."""
    if not qualities:  # Check if the list is empty
        return 0  # Or handle it differently if needed
    return sum(qualities) / len(qualities)

# Extract the top N reads from a FASTQ file based on average quality scores. Below example = 50, change it as you please.
def extract_top_reads(fastq_file, top_n=50):
    """Extract the top N reads from a FASTQ file based on average quality scores."""
    reads = []
    
    # Parse the FASTQ file and store reads with their average quality scores
    for record in SeqIO.parse(fastq_file, "fastq"):
        if "phred_quality" in record.letter_annotations:
            average_quality = calculate_average_quality(record.letter_annotations["phred_quality"])
        else:
            print(f"No quality scores found for record {record.id}")
            average_quality = 0
        reads.append((average_quality, record))
    
    # Sort reads by their average quality scores in descending order
    sorted_reads = sorted(reads, key=lambda x: x[0], reverse=True)
    
    # Select the top N reads
    top_reads = sorted_reads[:top_n]
    
    # Return only the sequence records of the top reads
    return [read[1] for read in top_reads]

def save_reads_to_fastq(reads, output_file):
    """Save a list of SeqRecord objects to a FASTQ file."""
    with open(output_file, "w") as output_handle:
        SeqIO.write(reads, output_handle, "fastq")

# Example usage
input_fastq = "/example.fastq"  # Path to the input FASTQ file
output_fastq = "/example.fastq"  # Path to the output FASTQ file

# Extract top 50 reads based on average quality scores. Change this as you please.
top_reads = extract_top_reads(input_fastq, top_n=50)

# Save the top reads to a new FASTQ file
save_reads_to_fastq(top_reads, output_fastq)
