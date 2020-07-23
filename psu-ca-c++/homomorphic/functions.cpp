#include "functions.h"

/* private function definitions */
int load_Data_into_BF(BloomFilter *bf,const char *filepath) {
    FILE *fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    fp = fopen(filepath, "r");
    if (fp == NULL) {
        fprintf(stderr, "Can't open file %s!\n", filepath);
        return 0;
    }

    int elementCount=0;

    while ((read = getline(&line, &len, fp)) != -1) {
        char *strip = line+1;
        strip[strlen(strip)-1]=0;

        char * pch= strtok(strip,", ");
        while (pch != NULL)
          {
            elementCount++;
            bloom_filter_add_string(bf, pch);
            pch = strtok(NULL, ", ");
          }
    }
    fclose(fp);
    if (line)
    free(line);

    return elementCount;
}

int encrypt_data_in_BF(BloomFilter *bf,mpz_t* paillier_pubKeys,mpz_t* ciphers){
    int curCount=0;
    for(int j=0;j<bf->bloom_length;j++){
        unsigned char *cur = bf->bloom+j;
        int slice;
        if(j < (bf->bloom_length-1) )
            slice=7;
        else
            slice=bf->number_bits-(bf->bloom_length-1)*8-1;

        for(int i=slice;i>=0;i--){
            if(!((*cur>>i) & 1)){//zero then encrypt with m=1
                mpz_init_set_ui(ciphers[curCount],1);
            }
            paillier_encryption(ciphers[curCount],paillier_pubKeys);
            curCount++;
        }
    }
    return 0;
}

void mpzArray_to_BinaryData(unsigned char** binaryData,mpz_t* data,int dataLen,int &byteCount,const char* toFilePath){
    size_t preAlloc= 4+ 4*dataLen;
    byteCount = preAlloc;

    for(u32 i = 0; i<dataLen; i++)
    {
        preAlloc += 8* data[i]->_mp_alloc;
    }

    
    *binaryData = (unsigned char *)malloc(preAlloc);
    memcpy(*binaryData,&dataLen,4);
    unsigned char* temp = *binaryData+4;

    for(u32 i = 0; i<dataLen; i++)
    {
        size_t count;
        unsigned char* data0 = (unsigned char *)mpz_export(temp+4,&count,1,1,1,0,data[i]);
        memcpy(temp,&count,4);
        temp += (count+4);
        byteCount += count;
    }

    if(toFilePath){
        FILE * pwFile;
        pwFile = fopen (toFilePath, "wb");
        fwrite (*binaryData , sizeof(unsigned char), byteCount, pwFile);
        fclose (pwFile);
    }
}

void load_binaryData_fromFile(unsigned char** binaryData,int &length,const char *filePath){
    FILE *pFile = fopen(filePath, "rb");
    fseek (pFile , 0 , SEEK_END);
    long lSize = ftell (pFile);
    rewind (pFile);
    *binaryData =(unsigned char*)malloc(lSize);
    length = lSize;
    fread(*binaryData,1,lSize,pFile);
    fclose(pFile);
}


void binaryData_to_mpzArray(unsigned char* binaryData,int outPutLen,mpz_t *outPut){
    unsigned char* temp=binaryData+4;
    for(u32 i = 0; i<outPutLen; i++)
    {
        int countBytes = *((int *)temp);
        mpz_import(outPut[i],countBytes,1,1,1,0,temp+4);
        temp += (4+countBytes);
    }
}


int load_cipherData(unsigned char** cipherData,int &dataLength,unsigned char** pubKeyData,int &pubBytesLen,
    unsigned char** priKeyData,int &priBytesLen,
    int &numbBits,int &numSlices,int &elementNum){

    const char cipherName[] = "../data/alice_ciphers.bin";
    const char pubKeyName[] = "../data/pubPallier.bin";
    const char priKeyName[] = "../data/priPallier.bin";

    const char bloomParameters[] = "../data/bloomParameters.txt";

    FILE *pFile = fopen(cipherName, "r");
    bool isExist = (pFile!=NULL);
    fclose(pFile);

    if(!isExist){
        BloomFilter bf;
        bloom_filter_init(&bf, ELEMENTS, FALSE_POSITIVE_RATE);
        elementNum = load_Data_into_BF(&bf, "../data/alice.data");
        bloom_filter_stats(&bf);

        mpz_t paillier_Keys[6];
        mpz_t pubKey[3],priKey[3];
        for(int i = 0; i < 6; i++)
        {
            mpz_init(paillier_Keys[i]);
            if(i<3)
            {
                mpz_init(pubKey[i]);
                mpz_init(priKey[i]);
            }
        }
        paillier_generateKeys(paillier_Keys);
        paillier_getPubKey(pubKey,paillier_Keys);
        paillier_getPriKey(priKey,paillier_Keys);


        int cipher_Len = bf.number_bits;
        mpz_t ciphers[cipher_Len];
        for(u32 i = 0; i<cipher_Len; i++)
        {
            mpz_init(ciphers[i]);
        }
        encrypt_data_in_BF(&bf,pubKey,ciphers);

        mpzArray_to_BinaryData(cipherData,ciphers,cipher_Len,dataLength,cipherName);
        mpzArray_to_BinaryData(pubKeyData,pubKey,3,pubBytesLen,pubKeyName);
        mpzArray_to_BinaryData(priKeyData,priKey,3,priBytesLen,priKeyName);


       FILE *fp;
       std::string content = std::to_string(bf.number_bits)+ "\n" 
       + std::to_string(bf.number_hashes)+"\n"
       + std::to_string(elementNum);
       fp = fopen(bloomParameters , "w" );
       fwrite(content.c_str() , 1 , content.size() , fp );
       fclose(fp);

       

       for(int i = 0; i<cipher_Len; i++)
        {
            mpz_clear(ciphers[i]);
        }
        bloom_filter_destroy(&bf);
        for(int i = 0; i < 6; i++)
        {
            mpz_clear(paillier_Keys[i]);
             if(i<3)
            {
                mpz_clear(pubKey[i]);
                mpz_clear(priKey[i]);
            }
        }
    }else{
        load_binaryData_fromFile(cipherData,dataLength,cipherName);
        load_binaryData_fromFile(pubKeyData,pubBytesLen,pubKeyName);
        load_binaryData_fromFile(priKeyData,priBytesLen,priKeyName);


        FILE *fp;
        char * line = NULL;
        size_t len = 0;
        ssize_t read;
        fp = fopen(bloomParameters, "r");
        if (fp == NULL) {
            fprintf(stderr, "Can't open file %s!\n", bloomParameters);
            return 0;
        }
        getline(&line, &len, fp);
        numbBits = atoi(line);

        getline(&line, &len, fp);
        numSlices = atoi(line);

        getline(&line, &len, fp);
        elementNum = atoi(line);

    // std::cout<<numbBits<<" fine is: "<<numSlices<<std::endl;



        fclose(fp);
        if (line)
        free(line);
    }
    return 1;
}


int calculate_Union_on_AliceData(mpz_t *bobCipher,int bobCipherLen,mpz_t pubKey[3],mpz_t priKey[3],mpz_t unionVal){

    BloomFilter bfAlice;
    bloom_filter_init(&bfAlice, ELEMENTS, FALSE_POSITIVE_RATE);
    load_Data_into_BF(&bfAlice, "data/alice.data");

    for(int i=0;i<bobCipherLen;i++){
        if(! bfAlice.bloom[i]){
            mpz_mul(unionVal,unionVal,bobCipher[i]);
            mpz_mod(unionVal,unionVal,pubKey[2]);
        }
    }

    return 1;
}