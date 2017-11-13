def main():
    #bestand = "Alpaca_mRNA.fna" # Voer hier de bestandsnaam van het juiste bestand in, of hernoem je bestand
    """
    Hier onder wordt de lees_inhoud functie aangeroepen om het bestand in te lezen en wordt met een try except
    structuur een FileNotFoundError afgevangen als het bestand niet bestaat. Als de file geen correcte fasta file is wordt
    er een exception opgeworpen die ook afgevangen wordt.
    """
    readCorrectly = False
    while readCorrectly == False:
        bestandsnaam = input("Please enter the name of the fasta file:\n")
        try:
            headers, seqs = lees_inhoud(bestandsnaam)
        except FileNotFoundError:
            print("The file you specified does not exist. Please choose a new one.")
        except:
            print("The file you specified is not a valid fasta file. Please choose a new one.")
        else:
            readCorrectly = True

    """
    Hier wordt een file met ezymen geopend. Als het bestand niet bestaat of de inhoud niet correct is wordt de exception afgevangen.
    De inhoud er van wordt met een for loop in een tweedimensionale array opgeslagen waarin enzym naam en sequentie,
    na het verwijderen van het "^" teken, aan elkaar gekoppeld zijn.
    """
    readCorrectly = False
    while readCorrectly == False:
        bestandsnaam = input("Please enter the name of the enzyme file:\n")
        try:
            enzym_file = open(bestandsnaam)

            lines = enzym_file.readlines()
            enzymen = []
            for line in lines:
                elements = line.split()
                elements[1] = elements[1].replace("^", "")
                if is_dna(elements[1]) != True:
                    raise Exception
                enzymen.append(elements)
        except FileNotFoundError:
            print("The file you specified does not exist, please enter a new one")
        except IndexError:
            print("The contents of the enzyme file are not correct, please enter a new one.")
        except:
            print("Not all sequences in the enzyme file are valid dna sequences, please enter a new one.")
        else:
            readCorrectly = True


    #Vraag de gebruiker om een woord waarop de headers doorzocht worden.
    zoekwoord = input("Geef een zoekwoord op: ")

    """
    Voor elke header wordt gekeken of het zoekwoord er in aanwezig is. Zo ja, dan wordt de header geprint. Daarna wordt met de is_dna
    functie gekeken of de bijbehorende sequentie alleen ATCG bevat. Als dat het geval is wordt voor elk enzym met de knipt functie gekeken of
    het wel of niet knipt in de sequentie. Dit wordt vervolgens geprint. Als de sequentie iets anders dan ATCG bevatte, dan wordt geprint dat
    de sequentie ongeldig is.
    """
    for x in range(len(headers)):
        if zoekwoord in headers[x]:
            print(headers[x].replace("\n", ""))
            if is_dna(seqs[x]):
                knipt_wel = []
                knipt_niet = []
                for y in range(len(enzymen)):
                    if knipt(enzymen[y][1], seqs[x]):
                        knipt_wel.append(enzymen[y][0])
                    else:
                        knipt_niet.append(enzymen[y][0])
                print("\tEnzymen die wel knippen in de sequentie: ")
                print("\t" + ", ".join(knipt_wel))
                print("\tEnzymen die niet knippen in de sequentie: ")
                print("\t" + ", ".join(knipt_niet))
            else:
                print("\tGeen geldige sequentie.")
                
    
    
def lees_inhoud(bestands_naam):
    bestand = open(bestands_naam)
    headers = []
    seqs = []

    sequentie = ""
    #While loop waarin constant de volgende regel wordt gelezen die blijft loopen tot de laatste regel is bereikt.
    line = bestand.readline()
    #Hier wordt gekeken of de eerste regel van het bestand met '>' begint. Anders wordt er een exception geraised omdat het geen fasta file is.
    if line.startswith(">") == False:
        raise Exception
    
    while line != "":
        #Als de regel een header is wordt hij aan de headers list toegevoegd, anders wordt de regel aan sequentie toegevoegd.
        if line.startswith(">"):
            headers.append(line)
        else:
            sequentie += line.strip()
        #Lees de volgende regel. Als dit een nieuwe header of het einde van de file is wordt sequentie aan de seqs list toegevoegd en wordt
        #sequentie weer leeg gemaakt.
        line = bestand.readline()
        if line.startswith(">") or line == "":
            seqs.append(sequentie)
            sequentie = ""
    bestand.close()
    return headers, seqs

    
def is_dna(seq):
    #Voor elk karakter wordt gekeken of het iets anders is dan ATCG. Zo ja, dan is dna False.
    for char in seq:
        char = char.upper()
        if char not in ['A', 'T', 'C', 'G']:
            return False
    return True
    

def knipt(enzym, seq):
    #Als het enzym aanwezig is in de sequentie wordt True gereturned, anders False.
    return enzym in seq

       
    
main()
