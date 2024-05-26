#include "helpers.h"
#include <stdio.h>
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Find the max RGB number
            float max = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0;
            if ((max - (int) max) > 0.4)
                max = (int) max + 1;
            else
                max = (int) max;

            // Grayscale
            image[i][j].rgbtBlue = max;
            image[i][j].rgbtGreen = max;
            image[i][j].rgbtRed = max;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int temp_rgbtBlue = 0;
    int temp_rgbtGreen = 0;
    int temp_rgbtRed = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j <= (width - 1) / 2; j++)
        {
            // Find the max RGB number
            temp_rgbtBlue = image[i][j].rgbtBlue;
            temp_rgbtGreen = image[i][j].rgbtGreen;
            temp_rgbtRed = image[i][j].rgbtRed;
            // Reverse
            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            image[i][width - 1 - j].rgbtBlue = temp_rgbtBlue;
            image[i][width - 1 - j].rgbtGreen = temp_rgbtGreen;
            image[i][width - 1 - j].rgbtRed = temp_rgbtRed;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int sum_B;
    int sum_G;
    int sum_R;
    int num;
    RGBTRIPLE copy[height][width];
    // Visit every image RGB nodes
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            num = 0;
            sum_B = 0;
            sum_G = 0;
            sum_R = 0;
            // Calculate the mean RGB numbers
            for (int k = i - 1; k <= i + 1; k++)
            {
                if ((k >= 0) && (k < height))
                {
                    for (int l = j - 1; l <= j + 1; l++)
                    {
                        if ((l >= 0) && (l < width))
                        {
                            num += 1;
                            sum_B += image[k][l].rgbtBlue;
                            sum_G += image[k][l].rgbtGreen;
                            sum_R += image[k][l].rgbtRed;
                        }
                    }
                }
            }
            // Rounding
            copy[i][j].rgbtBlue = (int) ((sum_B * 1.0 / num) + 0.5);
            copy[i][j].rgbtGreen = (int) ((sum_G * 1.0 / num) + 0.5);
            copy[i][j].rgbtRed = (int) ((sum_R * 1.0 / num) + 0.5);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int sum_B_x;
    int sum_G_x;
    int sum_R_x;
    int sum_B_y;
    int sum_G_y;
    int sum_R_y;
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    RGBTRIPLE copy[height][width];

    // Visit every image RGB nodes
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j <= width; j++)
        {
            sum_B_x = 0;
            sum_G_x = 0;
            sum_R_x = 0;
            sum_B_y = 0;
            sum_G_y = 0;
            sum_R_y = 0;
            // Apply the Sobel filter
            for (int k = i - 1; k <= i + 1; k++)
            {
                for (int l = j - 1; l <= j + 1; l++)
                {
                    if ((image[i][j].rgbtBlue == 255) && (image[i][j].rgbtGreen == 255) &&
                        (image[i][j].rgbtRed == 255))
                        continue;
                    if ((k >= 0) && (k < height) && (l >= 0) && (l < width))
                    {
                        sum_B_x += Gx[k - i + 1][l - j + 1] * image[k][l].rgbtBlue;
                        sum_G_x += Gx[k - i + 1][l - j + 1] * image[k][l].rgbtGreen;
                        sum_R_x += Gx[k - i + 1][l - j + 1] * image[k][l].rgbtRed;
                        sum_B_y += Gy[k - i + 1][l - j + 1] * image[k][l].rgbtBlue;
                        sum_G_y += Gy[k - i + 1][l - j + 1] * image[k][l].rgbtGreen;
                        sum_R_y += Gy[k - i + 1][l - j + 1] * image[k][l].rgbtRed;
                    }
                }
            }
            int temp_B = round(sqrt(sum_B_x * sum_B_x + sum_B_y * sum_B_y));
            int temp_G = round(sqrt(sum_G_x * sum_G_x + sum_G_y * sum_G_y));
            int temp_R = round(sqrt(sum_R_x * sum_R_x + sum_R_y * sum_R_y));
            // Set max pixel to 255
            if (temp_B > 255)
                copy[i][j].rgbtBlue = 255;
            else
                copy[i][j].rgbtBlue = temp_B;
            if (temp_G > 255)
                copy[i][j].rgbtGreen = 255;
            else
                copy[i][j].rgbtGreen = temp_G;
            if (temp_R > 255)
                copy[i][j].rgbtRed = 255;
            else
                copy[i][j].rgbtRed = temp_R;
        }
    }
    // Upload images
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}
