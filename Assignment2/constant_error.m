clc
clear
close all

p = 1:10;
predictions = zeros(1,length(p));

a = 3;
x_test = 0;


% numSamples taken from 'coeffs' in sim1. Dont know why this works
% but the results are fairly constant. Only in the beginning the estimation
% is 'too good'
for i = 1:length(p)
    nSamples = ceil(a * exp(p(i)));
    
    x_samples     = unifrnd(0, 1, [nSamples, p(i)]);
    x_samples_mag = sqrt(sum(x_samples.*x_samples, 2)); 
    y = exp(-a * x_samples_mag);

    x_closest = min(abs(x_samples_mag - x_test));
    predictions(i) = exp(-a * x_closest);

end

plot(p, 1-predictions);
xlabel('Number of dimensions');
ylabel('err_p')