clc
clear
close all

p = 1:32;
predictions = zeros(1,length(p));

a = 3;
x_test = 0;
nSamples = 1000;

for i = 1:length(p)
    
    x_samples     = unifrnd(0, 1, [nSamples, p(i)]);
    x_samples_mag = sqrt(sum(x_samples.*x_samples, 2)); 
    y = exp(-a * x_samples_mag);

    x_closest = min(abs(x_samples_mag - x_test));
    predictions(i) = exp(-a * x_closest);

end

figure
plot(p, predictions);

f = fit(p', predictions', 'exp1');

plot(f, p, predictions);
