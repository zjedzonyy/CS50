#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float avg;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            avg = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.00;
            image[i][j].rgbtBlue = round(avg);
            image[i][j].rgbtGreen = round(avg);
            image[i][j].rgbtRed = round(avg);
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{


    for (int i = 0; i < height; i++)
    {
       float sepiaRed = 0.00;
       float sepiaGreen = 0.00;
       float sepiaBlue = 0.00;

        for (int j = 0; j < width; j++)
        {
            sepiaRed = 0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue;
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            sepiaGreen = 0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue;
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            sepiaBlue = 0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue;
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[i][j].rgbtBlue = round(sepiaBlue);
            image[i][j].rgbtGreen = round(sepiaGreen);
            image[i][j].rgbtRed = round(sepiaRed);

        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][width-j-1];
            image[i][width-j-1] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];


    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
                float counts = 0.00;
                int totalRed = 0;
                int totalGreen = 0;
                int totalBlue = 0;

            // LOOP TO FIND WHICH PIXELS ARE VALID
            for (int a = -1; a < 2; a++)
            {

                for (int b = -1; b < 2; b++)
                {
                  int tempa = i + a;
                  int tempb = j + b;

                  if (tempa < 0 || tempb < 0 || tempa >= height || tempb >= width)
                  {
                    continue;
                  }


                     totalRed += image[tempa][tempb].rgbtRed;
                     totalGreen += image[tempa][tempb].rgbtGreen;
                     totalBlue += image[tempa][tempb].rgbtBlue;

                     counts++;

                }
                copy[i][j].rgbtRed = round(totalRed / counts);
                copy[i][j].rgbtGreen = round(totalGreen / counts);
                copy[i][j].rgbtBlue = round(totalBlue / counts);
            }
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = copy[i][j].rgbtRed;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
        }
    }
    return;
}
